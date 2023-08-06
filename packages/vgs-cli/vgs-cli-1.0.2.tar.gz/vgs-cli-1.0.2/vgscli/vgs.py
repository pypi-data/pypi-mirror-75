import click

from pkg_resources import iter_entry_points
from click_plugins import with_plugins

from vgscli import auth
from vgscli.api import create_api
from vgscli.auth import auto_login, handshake, token_util
from vgscli.errors import handle_errors
from vgscli.routes import dump_all_routes, sync_all_routes
from vgscli.utils import resolve_env


class Config(object):
    def __init__(self, debug, env):
        self.debug = debug
        self.env = env


@with_plugins(iter_entry_points('vgscli.plugins'))
@click.group()
@click.option("--debug", "-d", is_flag=True, help="Enables debug mode.", default=False)
@click.option("--environment", "-e", help="VGS environment.", hidden=True)
@click.version_option(message='%(version)s')
@click.pass_context
def cli(ctx, debug, environment):
    """
    Command Line Tool for programmatic configurations on VGS.
    """
    ctx.debug = debug

    env = resolve_env(environment)
    ctx.obj = Config(debug, env)

    auto_login(ctx, env)


@cli.command()
@click.argument("resource", type=click.Choice(['routes']))
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors
def get(ctx, resource, vault):
    """
    Get VGS resource.

    Possible resource values: routes
    """
    handshake(ctx, ctx.obj.env)

    if resource == "routes":
        vault_management_api = create_api(ctx, vault, ctx.obj.env, token_util.get_access_token())
        dump = dump_all_routes(vault_management_api)
        click.echo(dump)


@cli.command()
@click.argument("resource", type=click.Choice(['routes']))
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.option("--filename", "-f", help="Filename for the input data", type=click.File('r'), required=True)
@click.pass_context
def apply(ctx, resource, vault, filename):
    """
    Create or update VGS resource.

    Possible resource values: routes
    """
    handshake(ctx, ctx.obj.env)

    if resource == "routes":
        route_data = filename.read()
        vault_management_api = create_api(ctx, vault, ctx.obj.env, token_util.get_access_token())
        sync_all_routes(vault_management_api, route_data,
                        lambda route_id: click.echo(f'Route {route_id} processed'))
        click.echo(f'Routes updated successfully for vault {vault}')


@cli.command()
@click.pass_context
def login(ctx):
    """
    Login to VGS via browser.
    """
    auth.login(ctx, ctx.obj.env)


@cli.command()
@click.pass_context
def logout(ctx):
    """
    Logout from VGS.
    """
    auth.logout(ctx, ctx.obj.env)


if __name__ == "__main__":
    cli()
