import click

from .info import auth, info
from .labels import labels
from .milestones import milestones
from .release import release
from .remote import remote
from .validate import validate


@click.group(invoke_without_command=True)
@click.pass_context
def git(ctx):
    """Github client command repo management
    """
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


git.add_command(info)
git.add_command(auth)
git.add_command(labels)
git.add_command(milestones)
git.add_command(release)
git.add_command(remote)
git.add_command(validate)
