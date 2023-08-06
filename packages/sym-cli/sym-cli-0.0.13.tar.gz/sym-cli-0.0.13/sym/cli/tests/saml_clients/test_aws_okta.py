import pytest

from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = pytest.mark.usefixtures("click_context")


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsOkta]])
def test_aws_okta(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    with test_context(debug=False) as aws_okta:
        with capture_command():
            aws_okta.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command(
        "aws-okta exec sym -- aws ssm start-session --target i-0123456789abcdef"
    )


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsOkta]])
def test_aws_okta_debug(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    with test_context(debug=True) as aws_okta:
        with capture_command():
            aws_okta.exec("env")
    capture_command.assert_command("aws-okta --debug exec sym -- env")
