from typing import Type

import pytest

from sym.cli.providers import Provider
from sym.cli.providers.aws_okta import AwsOkta
from sym.cli.providers.chooser import ProviderName, choose_provider
from sym.cli.providers.saml2aws import Saml2Aws
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.mark.parametrize(
    argnames=("provider_name", "make_saml2aws", "expected"),
    argvalues=[
        ("auto", False, AwsOkta),
        ("auto", True, Saml2Aws),
        ("aws-okta", False, AwsOkta),
        ("aws-okta", True, AwsOkta),
        ("saml2aws", False, Saml2Aws),
        ("saml2aws", True, Saml2Aws),
    ],
)
def test_chooser(
    sandbox: Sandbox,
    provider_name: ProviderName,
    make_saml2aws: bool,
    expected: Type[Provider],
) -> None:
    if make_saml2aws:
        sandbox.create_file("bin/saml2aws", 0o755)
    with sandbox.push_exec_path():
        assert choose_provider(provider_name) == expected
