"""set_remote

The functionality for the jotter set-remote command.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import git

from jotter import util


def run(remote_url: str) -> None:
    """Run the set-remote command.
    
    Args:
        remote_url: The remote URL to use.
    """
    if not util.jotter_project_exists():
        print(
            "Unable to set remote, the current folder is not a jotter project."
        )
        raise SystemExit(1)

    repo = git.Repo(path=".")
    print("Setting remote...")
    if "origin" in repo.remotes:
        repo.remote("origin").set_url(remote_url)
    else:
        repo.create_remote("origin", remote_url)