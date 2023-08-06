from uuid import UUID

import pytest

from sym.cli.helpers.config import Config
from sym.cli.helpers.contexts import push_env
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def org(sandbox: Sandbox, uuid: UUID) -> str:
    org = uuid.hex
    with sandbox.create_file_with_content(".config/sym/config.yml") as f:
        print(f"org: {org}", file=f)
    return org


def test_get_org_with_xdg_config_home(sandbox: Sandbox, org: str) -> None:
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        assert Config()["org"] == org


def test_get_org_without_xdg_config_home(sandbox: Sandbox, org: str) -> None:
    with push_env("HOME", str(sandbox.path)):
        assert Config()["org"] == org
