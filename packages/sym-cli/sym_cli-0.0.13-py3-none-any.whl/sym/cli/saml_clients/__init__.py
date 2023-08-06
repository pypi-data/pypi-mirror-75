import re
import sys
from abc import abstractmethod
from configparser import ConfigParser
from typing import ClassVar, Protocol
from urllib.parse import urlsplit

from ..errors import CliError
from ..helpers import segment
from ..helpers.params import Profile, get_aws_saml_url, get_profile


class SAMLClient(Protocol):
    binary: ClassVar[str]
    resource: str
    debug: bool

    @abstractmethod
    def __init__(self, resource: str, *, debug: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def exec(self, *args: str, **opts: str) -> None:
        raise NotImplementedError

    def dprint(self, s: str):
        if self.debug:
            print(f"{s}\n")

    def dconfig(self, config: ConfigParser):
        if self.debug:
            print("Writing config:")
            config.write(sys.stdout)

    def log_subprocess_event(self, command: tuple):
        segment.track("Subprocess Called", binary=command[0])

    def get_profile(self) -> Profile:
        try:
            profile = get_profile(self.resource)
        except KeyError:
            raise CliError(f"Invalid resource: {self.resource}")

        self.dprint(f"Using profile {profile}")
        return profile

    def get_aws_saml_url(self, bare: bool = False) -> str:
        url = get_aws_saml_url(self.resource)
        if bare:
            url = urlsplit(url).path[1:]
        return url

    def get_creds(self):
        output = self.exec("env", capture_output_=True)[-1]
        env_vars = re.findall(r"([\w_]+)=(.+)\n", output)
        return {
            k: v
            for k, v in env_vars
            if k
            in (
                "AWS_REGION",
                "AWS_ACCESS_KEY_ID",
                "AWS_SECRET_ACCESS_KEY",
                "AWS_SESSION_TOKEN",
            )
        }
