from configparser import ConfigParser
from pathlib import Path
from typing import Final, Iterator, Tuple

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..errors import UnavailableRoleError
from ..helpers.config import SymConfigFile
from ..helpers.constants import AwsOktaNoRoles
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument
from ..helpers.params import get_aws_okta_params
from . import SAMLClient

ErrorPatterns = {AwsOktaNoRoles: UnavailableRoleError}

class AwsOkta(SAMLClient):
    __slots__ = ["aws_okta_cfg", "resource", "debug"]
    binary = "aws-okta"

    aws_okta_cfg: Final[SymConfigFile]
    resource: str
    debug: bool

    def __init__(self, resource: str, *, debug: bool) -> None:
        self.aws_okta_cfg = SymConfigFile("aws-okta.cfg")
        self.resource = resource
        self.debug = debug

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        self.log_subprocess_event(args)
        self._write_aws_okta_config()
        with push_env("AWS_CONFIG_FILE", str(self.aws_okta_cfg)):
            yield "aws-okta", {"debug": self.debug}, "exec", "sym", "--", *args, opts

    def _write_aws_okta_config(self) -> None:
        profile = self.get_profile()
        config = ConfigParser(default_section="okta")
        config.read_dict(
            {
                "okta": get_aws_okta_params(),
                "profile sym": {
                    "aws_saml_url": self.get_aws_saml_url(bare=True),
                    "region": profile.region,
                    "role_arn": profile.arn,
                },
            }
        )
        with self.aws_okta_cfg as f:
            config.write(f)

        self.dconfig(config)
