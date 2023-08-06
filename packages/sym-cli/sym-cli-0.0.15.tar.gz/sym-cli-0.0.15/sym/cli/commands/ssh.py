import click

from ..decorators import require_bins, require_login
from ..helpers.boto import host_to_instance
from ..helpers.ssh import start_ssh_session
from . import GlobalOptions
from .sym import sym


@sym.command(short_help="Start a SSH session")
@click.argument("resource")
@click.argument("host")
@click.option("--port", default=22, type=int, show_default=True)
@click.make_pass_decorator(GlobalOptions)
@require_bins("aws", "session-manager-plugin")
@require_login
def ssh(options: GlobalOptions, resource: str, host: str, port: int) -> None:
    """Use approved creds for RESOURCE to start a SSH session to an EC2 instance."""
    client = options.create_saml_client(resource)
    instance = host_to_instance(client, host)
    start_ssh_session(client, instance, port)
