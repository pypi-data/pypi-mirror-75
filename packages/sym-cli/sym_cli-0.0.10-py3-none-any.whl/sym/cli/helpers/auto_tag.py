from typing import Any, Callable

from click import Command, Context, Group
from sentry_sdk.api import push_scope


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def invoke(self, ctx: Context) -> Any:
        with push_scope() as scope:
            scope.set_tag("command", ctx.info_name)
            return super().invoke(ctx)


class AutoTagGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=AutoTagCommand)  # type: ignore
