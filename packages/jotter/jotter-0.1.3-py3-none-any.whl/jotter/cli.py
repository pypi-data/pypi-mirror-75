"""cli

The main CLI and entrypoint of jotter.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from typing import Optional

import click

import jotter as jotter_pkg
from jotter import init as init_cmd
from jotter import set_remote as set_remote_cmd
from jotter import sync as sync_cmd
from jotter import note as note_cmd

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
"""Context settings for Click."""


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(jotter_pkg.__version__)
def jotter():
    """Note taking and syncing utility."""


@jotter.command()
@click.argument("REMOTE_URL", required=False, type=str)
def init(remote_url: Optional[str] = None) -> None:
    """Initialise a new jotter project in the current directory."""
    init_cmd.run(remote_url)


@jotter.command()
@click.argument("REMOTE_URL", required=True, type=str)
def set_remote(remote_url: str) -> None:
    """Set the remote URL of the jotter project, for syncing."""
    set_remote_cmd.run(remote_url)


@jotter.command()
@click.argument("NOTE_FILE", required=False, type=str)
@click.option("-d", "--date", is_flag=True)
def note(note_file: Optional[str], date: bool) -> None:
    """Create or edit a jotter note."""
    note_cmd.run(note_file, date)


@jotter.command()
def sync() -> None:
    """Sync this jotter project with the remote."""
    sync_cmd.run()


def main():
    jotter()


if __name__ == "__main__":
    main()