from abc import abstractmethod
from typing import ClassVar, Protocol
from urllib.parse import urlsplit

from ..errors import CliError
from ..helpers.params import Profile, get_aws_saml_url, get_profile


class Provider(Protocol):
    binary: ClassVar[str]
    resource: str
    debug: bool

    @abstractmethod
    def __init__(self, resource: str, debug: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def exec(self, *args: str, **opts: str) -> None:
        raise NotImplementedError

    def get_profile(self) -> Profile:
        try:
            return get_profile(self.resource)
        except KeyError:
            raise CliError(f"Invalid resource: {self.resource}")

    def get_aws_saml_url(self, bare: bool = False) -> str:
        url = get_aws_saml_url(self.resource)
        if bare:
            url = urlsplit(url).path[1:]
        return url
