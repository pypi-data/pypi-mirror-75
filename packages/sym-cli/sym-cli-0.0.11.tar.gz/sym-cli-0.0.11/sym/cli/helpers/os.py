from os import X_OK, access, get_exec_path
from os.path import join as join_path
from pathlib import Path
from typing import TextIO


def safe_create(path: Path) -> TextIO:
    """
    Opens the given path in exclusive create mode (`"x"`), deleting the
    file beforehand if it already exists. This is the safe way to replace
    a file, that is not subject to symlink attacks.
    """

    path.unlink(missing_ok=True)
    return path.open("x")


def has_command(command: str) -> bool:
    """
    Returns whether the given command can be found on `PATH` and is
    executable.
    """

    return any(
        access(join_path(directory, command), X_OK) for directory in get_exec_path()
    )
