import click

from ..repo import RepoManager
from ..utils import command


@click.command()
@click.pass_context
def remote(ctx):
    """Display repo github path
    """
    with command():
        m = RepoManager(ctx.obj["agile"])
        click.echo(m.github_repo().repo_path)
