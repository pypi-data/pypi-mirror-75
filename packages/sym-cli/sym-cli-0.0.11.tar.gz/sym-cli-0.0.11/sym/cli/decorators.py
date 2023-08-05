import shlex
import subprocess
from functools import wraps
from subprocess import SubprocessError
from typing import Any, Callable, Iterator, Sequence, TypeVar, cast

from click import Command
from sentry_sdk.api import configure_scope
from sentry_sdk.hub import init as sentry_init

from .errors import CliError
from .helpers.config import Config
from .helpers.keywords_to_options import Argument, keywords_to_options
from .helpers.os import has_command
from .helpers.sentry import set_scope_context_os, set_scope_tag_org, set_scope_user

# Typing support for decorators is still in need of a lot of work:
# https://github.com/python/mypy/issues/3157. So the current grossness
# with casts is unavoidable for now.


F = TypeVar("F", bound=Callable[..., Any])
C = TypeVar("C", bound=Command)


def run_subprocess(
    func: Callable[..., Iterator[Sequence[Argument]]]
) -> Callable[..., None]:
    @wraps(func)
    def impl(*args: Any, **kwargs: Any) -> None:
        for command in func(*args, **kwargs):
            command = keywords_to_options(command)
            try:
                subprocess.run(command, check=True)
            except SubprocessError as err:
                raise CliError(f"Cannot run {shlex.join(command)}") from err

    return impl


# See: https://click.palletsprojects.com/en/7.x/commands/#decorating-commands


def require_bins(*bins: str) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            for binary in bins:
                if not has_command(binary):
                    raise CliError(f"Unable to find {binary} in your path!")
            return fn(*args, **kwargs)

        return cast(F, wrapped)

    return decorate


def require_login(fn: F) -> F:
    @wraps(fn)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        config = Config()
        if not config.get("org"):
            raise CliError("run sym login first")
        return fn(*args, **kwargs)

    return cast(F, wrapped)


def command_decorator(decorator: Callable[[F], F]) -> Callable[[C], C]:
    """
    A decorator that wraps a function decorator and returns a
    Click command decorator that applies the given decorator
    to the command's callback.
    """

    def decorate(cmd: C) -> C:
        if cmd.callback is not None:
            cmd.callback = decorator(cast(F, cmd.callback))
        return cmd

    return decorate


def setup_sentry(**kwargs: Any) -> Callable[[C], C]:
    sentry_init(**kwargs)

    @command_decorator
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            with configure_scope() as scope:
                set_scope_tag_org(scope)
                set_scope_user(scope)
                set_scope_context_os(scope)
                return fn(*args, **kwargs)

        return cast(F, wrapped)

    return decorator
