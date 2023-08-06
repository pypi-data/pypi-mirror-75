import logging
import os
from typing import Dict

import requests

from .components import GithubException
from .repo import GitRepo

__all__ = ["GithubApi", "GitRepo", "GithubException"]


LOGGER = logging.getLogger("github")


class GithubApi:
    def __init__(self, token: str = "") -> None:
        self.http = requests.Session()
        self.token = token or get_token()

    @property
    def api_url(self):
        return "https://api.github.com"

    @property
    def uploads_url(self):
        return "https://uploads.github.com"

    def __repr__(self):
        return self.api_url

    __str__ = __repr__

    def repo(self, repo_path):
        return GitRepo(self, repo_path)

    def default_headers(self) -> Dict[str, str]:
        headers = {}
        if self.token:
            headers["authorization"] = f"token {self.token}"
        return headers


def get_token() -> str:
    token = os.getenv("GITHUB_SECRET_TOKEN") or os.getenv("GITHUB_TOKEN")
    return token
