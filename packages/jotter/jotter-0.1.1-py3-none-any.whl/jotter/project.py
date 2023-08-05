"""project

Contains schemas and code for a jotter project file.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from dataclasses import dataclass, field
import platform
from typing import Mapping

from marshmallow import Schema, fields, post_load, ValidationError, EXCLUDE
import yaml

PROJECT_FILENAME = "jotterproject.yml"
"""The filename of a jotter project."""

DEFAULT_EDITORS = {"Windows": "notepad", "Darwin": "vi", "Linux": "vi"}
"""The default editors for the default platforms (Windows, OSX, Linux)."""


def default_editors() -> Mapping[str, str]:
    """Factory function for the default editor value in a Project."""
    return DEFAULT_EDITORS


class ProjectSchema(Schema):
    """Marshmallow schema for a Project object."""
    editor = fields.Mapping(keys=fields.Str,
                            values=fields.Str,
                            required=True,
                            allow_none=False)
    note_extension = fields.Str(required=True, allow_none=False, default="md")

    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)


@dataclass
class Project:
    """A jotter project.

    Attributes:
        editor: Mapping between platform.system() and default editor (i.e. 'vi').
        note_extension: File extension of notes. Default is 'md'.
    """
    editor: Mapping[str, str] = field(default_factory=default_editors)
    note_extension: str = "md"

    def get_editor(self) -> str:
        """Gets the editor command for the current platform.

        Raises:
            KeyError: If the platform wasn't listed in the editor dict.
        """
        current_platform = platform.system()
        try:
            return self.editor[current_platform]
        except KeyError:
            print(f"Unable to get editor for platform '{current_platform}'. "
                  "Please add it to the 'editor' dictionary in your project.")
            raise


def _print_validation_err(err: ValidationError, name: str) -> None:
    """Internal function used for printing a validation error in the Schema.
    Args:
        err (ValidationError): The error to log.
        name (str): A human-readable identifier for the Schema data source. 
            Like a filename.
    """
    # build up a string for each error
    log_str = []
    log_str.append(f"Error validating config '{name}':")
    for field_name, err_msgs in err.messages.items():
        log_str.append(f"{field_name}: {err_msgs}")

    # print the joined up string
    print(" ".join(log_str))


def load(project_path: str) -> Project:
    """Load a project from a YAML file.

    Args:
        project_path: The path to the project file.

    Returns:
        The loaded Project, or None if some error occurred.
    """
    try:
        with open(project_path, "r") as project_file:
            raw_project = yaml.safe_load(project_file)
            loaded_project = ProjectSchema(unknown=EXCLUDE).load(raw_project)
            return loaded_project
    except OSError as err:
        # there was some error opening the file
        print(f"Error opening project file: {err}")
        return None
    except yaml.YAMLError as err:
        # the YAML was malformed
        print(f"Error in project file: {err}")
        return None
    except ValidationError as err:
        # the project file was invalid
        _print_validation_err(err, project_path)
        return None


def dump(project: Project, project_path: str) -> None:
    """Dump a project to a YAML file.

    Args:
        project: The Project object to dump.
        project_path: The path to dump the project to.

    Raises:
        OSError: If there was some error writing the file.
    """
    try:
        with open(project_path, "w") as project_file:
            dumped_project = ProjectSchema().dump(project)
            yaml.safe_dump(dumped_project, project_file)
    except OSError as err:
        # there was some error writing the file
        print(f"Error writing project file: {err}")
        raise