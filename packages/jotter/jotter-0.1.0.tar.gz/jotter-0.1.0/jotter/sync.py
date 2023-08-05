"""sync

Implements the sync command of jotter.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import git

from jotter import util


def run() -> None:
    """Run the sync command."""
    if not util.jotter_project_exists():
        print("Unable to sync, the current folder is not a jotter project.")
        raise SystemExit(1)

    repo = git.Repo(path=".")
    if "origin" not in repo.remotes:
        print("Unable to sync, repo did not have remote. "
              "Have you run jotter set-remote?")
        raise SystemExit(1)

    print("Syncing...")
    try:
        if len(repo.remote().refs) > 0:
            repo.remote().pull("master")
        repo.remote().push("master")
    except git.GitError as err:
        print(f"Unable to sync, {err}")
        raise SystemExit(1)
