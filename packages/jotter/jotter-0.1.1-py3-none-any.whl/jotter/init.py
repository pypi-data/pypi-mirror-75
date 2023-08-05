"""init

Contains jotter functionality specific to the init command.

Author
    Figglewatts <me@figglewatts.co.uk>
"""
from os import path
from typing import Optional

import git

from jotter import project, util


def run(remote_url: Optional[str] = None) -> None:
    """Run the init command.

    Will exit the program if the current folder is already a git repo.

    Args:
        remote_url: The optional remote URL to clone from.
    """
    if util.jotter_project_exists():
        print("Unable to init project, this folder is already a jotter "
              "project or git repo.")
        raise SystemExit(1)

    if not remote_url:
        create_new()
    else:
        clone_existing(remote_url)


def create_new() -> None:
    """Create a new jotter project in the current directory."""
    if path.exists(".git"):
        print(
            "Unable to create new project, this folder is already a git repo.")
        raise SystemExit(1)

    print("Creating project...")
    proj = project.Project()
    project.dump(proj, project.PROJECT_FILENAME)

    print("Creating repository...")
    repo = git.Repo.init()

    print("Creating commit...")
    repo.index.add(repo.untracked_files)
    repo.index.commit("Initial commit")
    repo.create_head("master")


def clone_existing(remote_url: str) -> None:
    pass