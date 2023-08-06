import click

from ..decorators import require_login
from ..helpers.params import get_profiles
from .sym import sym


@sym.command(short_help="list available resource groups")
@require_login
def resources() -> None:
    """List resource groups available for use"""
    for (slug, profile) in get_profiles().items():
        click.echo(f"{slug} ({profile.display_name})")
