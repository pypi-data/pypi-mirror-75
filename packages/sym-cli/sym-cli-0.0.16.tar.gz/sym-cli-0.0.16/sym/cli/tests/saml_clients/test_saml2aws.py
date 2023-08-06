import pytest

from sym.cli.saml_clients.saml2aws import Saml2Aws
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = pytest.mark.usefixtures("click_context")


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[Saml2Aws]])
def test_saml2aws(
    test_context: TestContextFixture[Saml2Aws], capture_command: CaptureCommand
) -> None:
    with test_context(debug=False) as saml2aws:
        with capture_command():
            saml2aws.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command(
        f"saml2aws --config {saml2aws.saml2aws_cfg} --idp-account sym login",
        f"saml2aws --config {saml2aws.saml2aws_cfg} --idp-account sym exec -- 'aws ssm start-session --target i-0123456789abcdef'",
    )


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[Saml2Aws]])
def test_saml2aws_debug(
    test_context: TestContextFixture[Saml2Aws], capture_command: CaptureCommand
) -> None:
    with test_context(debug=True) as saml2aws:
        with capture_command():
            saml2aws.exec("env")
    capture_command.assert_command(
        f"saml2aws --verbose --config {saml2aws.saml2aws_cfg} --idp-account sym login",
        f"saml2aws --verbose --config {saml2aws.saml2aws_cfg} --idp-account sym exec -- env",
    )
