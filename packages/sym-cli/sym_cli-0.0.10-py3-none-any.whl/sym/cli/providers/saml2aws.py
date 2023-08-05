from configparser import ConfigParser
from pathlib import Path
from typing import Final, Iterator, Tuple

from ..decorators import require_bins, run_subprocess
from ..helpers.config import sym_config_file
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument, Options
from ..helpers.os import safe_create
from ..helpers.params import get_saml2aws_params
from . import Provider


class Saml2Aws(Provider):
    __slots__ = ["saml2aws_cfg", "resource", "debug"]
    binary = "saml2aws"

    saml2aws_cfg: Final[Path]
    resource: str
    debug: bool

    def __init__(self, resource: str, debug: bool) -> None:
        self.saml2aws_cfg = sym_config_file("saml2aws.cfg")
        self.resource = resource
        self.debug = debug

    @run_subprocess
    @require_bins(binary)
    def exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        s2a_options: Options = {
            "verbose": self.debug,
            "config": str(self.saml2aws_cfg),
            "idp_account": "sym",
        }
        config = self._write_saml2aws_config()
        with push_env("AWS_REGION", config["sym"]["region"]):
            yield "saml2aws", s2a_options, "login"  # no-op if session active
            yield "saml2aws", s2a_options, "exec", "--", *args, opts

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
        with safe_create(self.saml2aws_cfg) as f:
            config.write(f)
        return config
