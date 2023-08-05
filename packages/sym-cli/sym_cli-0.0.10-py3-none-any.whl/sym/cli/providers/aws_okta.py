from configparser import ConfigParser
from pathlib import Path
from typing import Final, Iterator, Tuple

from ..decorators import require_bins, run_subprocess
from ..helpers.config import sym_config_file
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument
from ..helpers.os import safe_create
from ..helpers.params import get_aws_okta_params
from . import Provider


class AwsOkta(Provider):
    __slots__ = ["aws_okta_cfg", "resource", "debug"]
    binary = "aws-okta"

    aws_okta_cfg: Final[Path]
    resource: str
    debug: bool

    def __init__(self, resource: str, debug: bool) -> None:
        self.aws_okta_cfg = sym_config_file("aws-okta.cfg")
        self.resource = resource
        self.debug = debug

    @run_subprocess
    @require_bins(binary)
    def exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
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
        with safe_create(self.aws_okta_cfg) as f:
            config.write(f)
