import json

import click

from ..utils import gitrepo
from .utils import repo_manager


@click.command()
def info():
    """Display information about repository
    """
    info = gitrepo()
    click.echo(json.dumps(info, indent=4))


@click.command()
@click.pass_context
def auth(ctx):
    """Display github token
    """
    repo = repo_manager(ctx)
    click.echo(repo.github.token)
