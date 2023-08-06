from typing import Literal, Type

from ..helpers.os import has_command
from . import SAMLClient
from .aws_okta import AwsOkta
from .saml2aws import Saml2Aws

SAMLClientName = Literal["auto", "aws-okta", "saml2aws"]


def choose_saml_client(saml_client_name: SAMLClientName) -> Type[SAMLClient]:
    if saml_client_name == "aws-okta":
        return AwsOkta
    elif saml_client_name == "saml2aws":
        return Saml2Aws
    else:
        return Saml2Aws if has_command("saml2aws") else AwsOkta
