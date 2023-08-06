from unittest import mock

from agiletoolkit.repo import RepoManager
from agiletoolkit.test import gitrepo


def test_message():
    with gitrepo("slack"):
        m = RepoManager()
        with mock.patch("click.secho") as p:
            m.message("test")
            assert p.called
