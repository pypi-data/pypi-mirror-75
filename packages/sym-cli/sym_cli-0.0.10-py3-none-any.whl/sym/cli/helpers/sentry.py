from getpass import getuser
from os import uname

from sentry_sdk.scope import Scope

from .config import Config


def set_scope_tag_org(scope: Scope) -> None:
    try:
        # TODO: Should we make Config a singleton?
        # Right now each instance rereads the YAML.
        scope.set_tag("org", Config().get_org())
    except KeyError:
        pass


def set_scope_user(scope: Scope) -> None:
    try:
        scope.set_user({"username": getuser()})
    except KeyError:
        pass


def set_scope_context_os(scope: Scope) -> None:
    u = uname()
    uname_str = f"{u.sysname} {u.nodename} {u.release} {u.version} {u.machine}"
    scope.set_context(
        "os",
        {
            "name": u.sysname,
            "version": u.release,
            "build": u.version,
            "kernel_version": uname_str,
        },
    )
