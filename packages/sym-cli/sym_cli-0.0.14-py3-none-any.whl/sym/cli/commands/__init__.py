import importlib
from pathlib import Path
from typing import Type

import click

from ..helpers import segment
from ..saml_clients import SAMLClient


class GlobalOptions:
    saml_client_type: Type[SAMLClient]
    debug: bool = False

    def create_saml_client(self, resource: str) -> SAMLClient:
        segment.track("Resource Requested", resource=resource)
        return self.saml_client_type(resource, debug=self.debug)

    def to_dict(self):
        return {"debug": self.debug, "saml_client": self.saml_client_type.__name__}


for path in Path(__file__).resolve().parent.glob("*.py"):
    if path.stem != "__init__":
        importlib.import_module(f".{path.stem}", __name__)
