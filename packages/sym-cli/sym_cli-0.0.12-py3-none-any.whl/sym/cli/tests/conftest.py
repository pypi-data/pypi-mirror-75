from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Iterator
from uuid import UUID, uuid4

import pytest
from _pytest.monkeypatch import MonkeyPatch

from sym.cli.helpers.config import Config
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def uuid() -> UUID:
    return uuid4()


@pytest.fixture
def uuid_factory() -> Callable[[], UUID]:
    return uuid4


CustomOrgFixture = Callable[[str], ContextManager[None]]


@pytest.fixture
def custom_org(monkeypatch: MonkeyPatch) -> CustomOrgFixture:
    @contextmanager
    def custom_org(org: str) -> Iterator[None]:
        with monkeypatch.context() as mp:
            mp.setattr(Config, "get_org", lambda self: org)
            yield

    return custom_org


@pytest.fixture
def capture_command(monkeypatch: MonkeyPatch) -> CaptureCommand:
    return CaptureCommand(monkeypatch)
