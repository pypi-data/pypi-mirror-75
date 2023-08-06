import shlex
from configparser import ConfigParser
from pathlib import Path
from typing import Final, Iterator, Tuple

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..errors import UnavailableRoleError
from ..helpers.config import SymConfigFile
from ..helpers.constants import Saml2AwsNoRoles
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument, Options, keywords_to_options
from ..helpers.params import get_saml2aws_params
from . import SAMLClient

ErrorPatterns = {Saml2AwsNoRoles: UnavailableRoleError}


class Saml2Aws(SAMLClient):
    __slots__ = ["saml2aws_cfg", "resource", "debug"]
    binary = "saml2aws"

    saml2aws_cfg: Final[SymConfigFile]
    resource: str
    debug: bool

    def __init__(self, resource: str, *, debug: bool) -> None:
        self.saml2aws_cfg = SymConfigFile("saml2aws.cfg")
        self.resource = resource
        self.debug = debug

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        self.log_subprocess_event(args)
        s2a_options: Options = {
            "verbose": self.debug,
            "config": str(self.saml2aws_cfg),
            "idp_account": "sym",
        }
        config = self._write_saml2aws_config()
        # saml2aws exec actually joins all the arguments into a single string and
        # runs it with the shell. So we have to use shlex.join to get around that!
        reparseable = shlex.join(keywords_to_options([*args, opts]))
        with push_env("AWS_REGION", config["sym"]["region"]):
            yield "saml2aws", s2a_options, "login"  # no-op if session active
            yield "saml2aws", s2a_options, "exec", "--", reparseable

    def _write_saml2aws_config(self) -> ConfigParser:
        profile = self.get_profile()
        saml2aws_params = get_saml2aws_params()
        config = ConfigParser()
        config.read_dict(
            {
                "sym": {
                    "url": self.get_aws_saml_url(),
                    "provider": "Okta",
                    "skip_verify": "false",
                    "timeout": "0",
                    "aws_urn": "urn:amazon:webservices",
                    **saml2aws_params,
                    "role_arn": profile.arn,
                    "region": profile.region,
                }
            }
        )
        with self.saml2aws_cfg as f:
            config.write(f)

        self.dconfig(config)

        return config
