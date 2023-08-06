from contextlib import contextmanager

import pytest
from click.testing import CliRunner

from sym.cli.helpers.config import Config
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def click_setup(sandbox: Sandbox):
    @contextmanager
    def context(set_org=True):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                sandbox.create_binary(f"bin/{AwsOkta.binary}")
                with sandbox.push_exec_path():
                    if set_org:
                        Config.instance()["org"] = "sym"
                    yield runner

    return context


def test_login(click_setup):
    with click_setup(set_org=False) as runner:
        result = runner.invoke(
            click_command, ["login", "--org", "sym", "--email", "y@symops.io"]
        )
        assert result.exit_code == 0
        assert result.output == "Sym successfully initalized!\n"


def test_resources(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["resources"])
        assert result.exit_code == 0
        assert result.output == "chris (Chris)\njon (Jon)\n"


def test_ssh(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["exec", "jon", "--", "aws"])
        assert result.exit_code == 0
