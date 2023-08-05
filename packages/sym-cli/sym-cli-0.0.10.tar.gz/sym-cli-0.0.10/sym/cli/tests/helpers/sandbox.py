from contextlib import contextmanager
from os import fchmod
from pathlib import Path
from typing import Iterator, TextIO

from sym.cli.helpers.contexts import push_env


class Sandbox:
    def __init__(self, path: Path) -> None:
        self.path = path

    def create_file(self, name: str, mode: int = 0o644) -> None:
        with self.create_file_with_content(name, mode):
            pass

    @contextmanager
    def create_file_with_content(
        self, name: str, mode: int = 0o644
    ) -> Iterator[TextIO]:
        path = self.path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x") as f:
            fchmod(f.fileno(), mode)
            yield f

    @contextmanager
    def push_exec_path(self) -> Iterator[None]:
        with push_env("PATH", str(self.path / "bin")):
            yield

    @contextmanager
    def push_xdg_config_home(self) -> Iterator[None]:
        with push_env("XDG_CONFIG_HOME", str(self.path / ".config")):
            yield
