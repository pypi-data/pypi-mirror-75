import os
import shlex
import subprocess
import sys
from functools import wraps
from subprocess import PIPE, CalledProcessError
from typing import (
    Any,
    Callable,
    Iterator,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    Type,
    TypeVar,
    cast,
)

import analytics
import click
from sentry_sdk.api import configure_scope
from sentry_sdk.hub import init as sentry_init

from .commands import GlobalOptions
from .errors import CliError, FailedSubprocessError, SuppressedError
from .helpers import segment
from .helpers.config import Config
from .helpers.keywords_to_options import Argument, keywords_to_options
from .helpers.os import has_command
from .helpers.sentry import set_scope_context_os, set_scope_tag_org, set_scope_user

# Typing support for decorators is still in need of a lot of work:
# https://github.com/python/mypy/issues/3157. So the current grossness
# with casts is unavoidable for now.


F = TypeVar("F", bound=Callable[..., Any])


def run_subprocess(
    func: Callable[..., Iterator[Sequence[Argument]]]
) -> Callable[..., Optional[Sequence[Optional[str]]]]:
    @wraps(func)
    @click.make_pass_decorator(GlobalOptions)
    def impl(
        options: GlobalOptions, *args: Any, capture_output_=False, **kwargs: Any
    ) -> Optional[Sequence[Optional[str]]]:
        outputs = []
        for command in func(*args, **kwargs):
            command = keywords_to_options(command)
            if options.debug:
                print(f"exec: {shlex.join(command)}\n")
            result = subprocess.run(
                command,
                check=True,
                capture_output=capture_output_,
                stderr=None if capture_output_ else PIPE,
                text=True,
            )
            outputs.append(result.stdout)
        if capture_output_:
            return outputs

    return impl


def intercept_errors(
    patterns: Mapping[Pattern[str], Type[Exception]] = {},
    *,
    quiet: bool = False,
    suppress: bool = False,
) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(
            *args: Any, quiet_: bool = False, suppress_: bool = False, **kwargs: Any
        ) -> Any:
            try:
                return fn(*args, **kwargs)
            except CalledProcessError as err:
                message = err.stderr
                if error := next(
                    (
                        error
                        for pattern, error in patterns.items()
                        if pattern.search(message)
                    ),
                    None,
                ):
                    raise error
                if not (quiet or quiet_):
                    sys.stderr.write(message)
                if suppress or suppress_:
                    raise SuppressedError(shlex.join(err.cmd)) from err
                else:
                    raise FailedSubprocessError(shlex.join(err.cmd)) from err

        return cast(F, wrapped)

    return decorate


# See: https://click.palletsprojects.com/en/7.x/commands/#decorating-commands


def require_bins(*bins: str) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            for binary in bins:
                if not has_command(binary):
                    raise CliError(f"Unable to find {binary} in your path!")
            return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorate


def require_login(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        config = Config.instance()
        if "org" not in config:
            raise CliError("Please run `sym login` first")
        return context.invoke(fn, *args, **kwargs)

    return cast(F, wrapped)


def setup_segment(**kwargs: Any) -> Callable[[F], F]:
    analytics.default_client = analytics.client.Client(**kwargs)

    def decorator(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            segment.identify()
            return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorator


def setup_sentry(**kwargs: Any) -> Callable[[F], F]:
    sentry_init(**kwargs)

    def decorator(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            with configure_scope() as scope:
                set_scope_tag_org(scope)
                set_scope_user(scope)
                set_scope_context_os(scope)
                return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorator
