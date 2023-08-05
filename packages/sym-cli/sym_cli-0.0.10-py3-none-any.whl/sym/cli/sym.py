from typing import Tuple, Type

import click

from .decorators import require_bins, require_login, setup_sentry
from .errors import CliError
from .helpers.auto_tag import AutoTagGroup
from .helpers.config import Config
from .helpers.constants import SENTRY_DSN
from .helpers.params import PARAMS, get_profiles
from .providers import Provider
from .providers.chooser import ProviderName, choose_provider
from .version import __version__


class GlobalOptions:
    provider_type: Type[Provider]
    debug: bool

    def create_provider(self, resource: str) -> Provider:
        return self.provider_type(resource, self.debug)


@setup_sentry(dsn=SENTRY_DSN, release=f"sym-cli@{__version__}")
@click.group(cls=AutoTagGroup)
@click.option(
    "--provider",
    "provider_name",
    default="auto",
    type=click.Choice(["auto", "aws-okta", "saml2aws"]),
    help="the provider type to use",
)
@click.option("--debug", is_flag=True, help="enable verbose debugging")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def sym(options: GlobalOptions, provider_name: ProviderName, debug: bool) -> None:
    """Access resources managed by Sym workflows.

    Use these tools to work with your resources once you've gotten approval in
    Slack.
    """

    options.provider_type = choose_provider(provider_name)
    options.debug = debug


@sym.command(short_help="print the version")
def version() -> None:
    click.echo(__version__)


@sym.command(short_help="login to your sym account")
@click.option("--org", help="org slug", prompt=True)
def login(org: str) -> None:
    """Link your Sym account"""
    if org not in PARAMS:
        raise CliError(f"Invalid org: {org}")
    config = Config()
    config["org"] = org


@sym.command(short_help="list available resource groups")
@require_login
def resources() -> None:
    """List resource groups available for use"""
    for (slug, profile) in get_profiles().items():
        click.echo(f"{slug} ({profile.display_name})")


@sym.command(short_help="ssh to an ec2 instance")
@click.argument("resource")
@click.option(
    "--target", help="target instance id", metavar="<instance-id>", required=True
)
@click.make_pass_decorator(GlobalOptions)
@require_bins("session-manager-plugin")
@require_login
def ssh(options: GlobalOptions, resource: str, target: str) -> None:
    """Use approved creds for RESOURCE to ssh to an ec2 instance"""
    options.create_provider(resource).exec("aws", "ssm", "start-session", target=target)


@sym.command("exec", short_help="execute a command")
@click.argument("resource")
@click.argument("command", nargs=-1)
@click.make_pass_decorator(GlobalOptions)
@require_login
def sym_exec(options: GlobalOptions, resource: str, command: Tuple[str, ...]) -> None:
    """Use approved creds for RESOURCE to execute COMMAND"""
    options.create_provider(resource).exec(*command)
