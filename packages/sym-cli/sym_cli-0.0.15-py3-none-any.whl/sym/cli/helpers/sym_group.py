from typing import Any, Callable

from click import Command, Context, Group
from sentry_sdk.api import push_scope

from . import segment
from .validations import validate_resource


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def invoke(self, ctx: Context) -> Any:
        segment.track(
            "Command Executed", command=ctx.info_name, options=ctx.obj.to_dict()
        )
        with push_scope() as scope:
            scope.set_tag("command", ctx.info_name)
            scope.set_extra("options", ctx.obj.to_dict())
            return super().invoke(ctx)

    def parse_args(self, ctx, args):
        if (
            self.params
            and (resource := ctx.parent.params.get("resource"))
            and self.params[0].name == "resource"
            and (not args or not validate_resource(args[0]))
        ):
            args = [resource] + args
        return super().parse_args(ctx, args)


class SymGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def parse_args(self, ctx, args):
        return super().parse_args(ctx, args)

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=AutoTagCommand)  # type: ignore
