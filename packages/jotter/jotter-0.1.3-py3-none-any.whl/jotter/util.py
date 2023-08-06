"""util

Contains various utility functions for jotter.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from os import path

from jotter import project


def jotter_project_exists() -> bool:
    """Ensure that a jotter project exists in the current path.

    Checks for a git repository (.git folder), and a jotter project file.

    Returns:
        True if a project exists, False otherwise.
    """
    return path.exists(".git") and path.exists(project.PROJECT_FILENAME)