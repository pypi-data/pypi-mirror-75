from typing import Tuple

import click

from ..decorators import require_bins, require_login
from ..helpers.ansible import run_ansible
from . import GlobalOptions
from .sym import sym


@sym.command(
    short_help="Run an Ansible command",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("resource")
@click.argument("command", nargs=-1)
@click.make_pass_decorator(GlobalOptions)
@require_bins("ansible", "aws", "session-manager-plugin")
@require_login
def ansible(options: GlobalOptions, resource: str, command: Tuple[str, ...]) -> None:
    """Use approved creds for RESOURCE to run an Ansible command."""
    client = options.create_saml_client(resource)
    run_ansible(client, command)
