from typing import Literal, Type

from ..helpers.os import has_command
from . import Provider
from .aws_okta import AwsOkta
from .saml2aws import Saml2Aws

ProviderName = Literal["auto", "aws-okta", "saml2aws"]


def choose_provider(provider_name: ProviderName) -> Type[Provider]:
    if provider_name == "aws-okta":
        return AwsOkta
    elif provider_name == "saml2aws":
        return Saml2Aws
    else:
        return Saml2Aws if has_command("saml2aws") else AwsOkta
