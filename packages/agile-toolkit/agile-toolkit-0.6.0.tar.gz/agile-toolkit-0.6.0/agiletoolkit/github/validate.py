import click

from ..api import GithubException
from .utils import repo_manager


@click.command()
@click.option(
    "--sandbox",
    is_flag=True,
    help="Validate only on sandbox/deploy branch",
    default=False,
)
@click.option(
    "--yes-no",
    is_flag=True,
    help="Return yes for version is good, no for version is not good",
    default=False,
)
@click.pass_context
def validate(ctx, sandbox, yes_no):
    """Check if version of repository is semantic
    """
    m = repo_manager(ctx)
    if not sandbox or m.can_release("sandbox"):
        try:
            version = m.validate_version()
            click.echo("yes" if yes_no else version)
        except GithubException:
            if yes_no:
                return click.echo("no")
            raise
