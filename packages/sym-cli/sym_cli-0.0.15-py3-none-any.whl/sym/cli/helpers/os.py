from contextlib import contextmanager
from os import X_OK, access, get_exec_path, link
from os.path import join as join_path
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TextIO


@contextmanager
def safe_create(path: Path) -> TextIO:
    """
    Opens the given path in exclusive create mode (`"x"`), deleting the
    file beforehand if it already exists. This is the safe way to replace
    a file, that is not subject to symlink attacks.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", dir=str(path.parent)) as f:
        yield f
        path.unlink(missing_ok=True)
        link(f.name, str(path))


def has_command(command: str) -> bool:
    """
    Returns whether the given command can be found on `PATH` and is
    executable.
    """

    return any(
        access(join_path(directory, command), X_OK) for directory in get_exec_path()
    )
