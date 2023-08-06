"""note

Functionality for the jotter note command.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from datetime import datetime
from os import path
import subprocess
from typing import Optional

import git

from jotter import util, project


def run(note_filename: Optional[str], date: bool) -> None:
    """Run the note command.

    Args:
        note_filename: The filename of the note.
        date: Prepend a date to the given filename.
    """
    if not note_filename and not date:
        print(
            "You need to specify a note filename to create a note. "
            "You can also specify --date to make the filename the current date."
        )
        raise SystemExit(1)

    if not util.jotter_project_exists():
        print(
            "Unable to create note, the current folder is not a jotter project."
        )
        raise SystemExit(1)
    proj = project.load(project.PROJECT_FILENAME)

    if not note_filename:
        note_filename = ""

    if date:
        date_str = datetime.now().strftime("%Y-%m-%d")
        note_filename = f"{date_str}{note_filename}"

    # if note doesn't have file extension, add the one specified in project
    if "." not in note_filename:
        note_filename += f".{proj.note_extension}"

    # if the node doesn't exist, create it first
    editing = True
    if not path.exists(note_filename):
        editing = False
        create_note(note_filename)

    # launch subprocess to edit
    try:
        editor = proj.get_editor()
    except KeyError:
        raise SystemExit(1)
    subprocess.run([editor, note_filename])

    try:
        repo = git.Repo(path=".")
        repo.index.add([note_filename])
        commit_action_word = "Edit" if editing else "Create"
        repo.index.commit(f"{commit_action_word} {note_filename}")
    except git.GitError as err:
        print(f"Unable to create note, {err}")
        raise SystemExit(1)


def create_note(note_filename: str) -> None:
    """Create a note at a given file path.
    
    Exits program if there was some error.
    """
    try:
        open(note_filename, "w").close()
    except OSError as err:
        print(f"Unable to create note, {err}")
        raise SystemExit(1)