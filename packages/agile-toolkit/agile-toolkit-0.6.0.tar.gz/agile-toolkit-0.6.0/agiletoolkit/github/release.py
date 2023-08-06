import click

from ..utils import niceJson
from .utils import repo_manager


@click.command()
@click.option("--yes", is_flag=True, help="Commit changes to github", default=False)
@click.option(
    "--latest", is_flag=True, help="Show latest release in github", default=False
)
@click.pass_context
def release(ctx, yes, latest):
    """Create a new release in github
    """
    m = repo_manager(ctx)
    api = m.github_repo()
    if latest:
        latest = api.releases.latest()
        if latest:
            click.echo(latest["tag_name"])
        else:
            click.echo("no releases")
    elif m.can_release("sandbox"):
        branch = m.info["branch"]
        version = m.validate_version()
        name = "v%s" % version
        body = ["Release %s from agiletoolkit" % name]
        data = dict(
            tag_name=name,
            target_commitish=branch,
            name=name,
            body="\n\n".join(body),
            draft=False,
            prerelease=False,
        )
        if yes:
            data = api.releases.create(data=data)
            m.message("Successfully created a new Github release")
        click.echo(niceJson(data))
    else:
        click.echo("skipped")
