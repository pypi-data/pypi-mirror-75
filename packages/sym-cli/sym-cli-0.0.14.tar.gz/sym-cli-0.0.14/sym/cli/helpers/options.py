import click

from .config import Config
from .validations import validate_resource


def config_option(name: str, help: str):
    def decorator(f):
        option_decorator = click.option(
            f"--{name}",
            help=help,
            prompt=True,
            default=lambda: Config.instance().get(name),
        )
        return option_decorator(f)

    return decorator


def _resource_callback(ctx, resource: str):
    if resource is None:
        return None
    if not validate_resource(resource):
        raise click.BadParameter(f"Invalid resource: {resource}")
    return resource


def resource_option(f):
    option_decorator = click.option(
        "--resource",
        help="the Sym resource to use",
        envvar="SYM_RESOURCE",
        callback=_resource_callback,
        default=Config.instance().get('default_resource'),
    )
    return option_decorator(f)
