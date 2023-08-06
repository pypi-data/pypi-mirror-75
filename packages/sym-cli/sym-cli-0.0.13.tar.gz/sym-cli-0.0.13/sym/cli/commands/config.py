import click

from ..errors import CliError
from ..helpers.config import Config, ConfigSchema
from .sym import sym


def _key_callback(ctx, key: str):
    if key not in ConfigSchema.__annotations__:
        raise click.BadParameter(key)
    return key


@sym.command(short_help="get and set config values")
@click.argument("key", callback=_key_callback)
@click.argument("value", required=False)
def config(key: str, value: str) -> None:
    """Get and set Sym config values."""
    if value:
        Config.instance()[key] = value
    else:
        click.echo(Config.instance().get(key))
