"""
Commands
"""

# import os
# import pathlib
# import shutil
# import zipfile

import shlex
import subprocess

from ..external import click

TITLE = "ZMAG"
DESCRIPTION = "Craft APIs with ZeroMQ and GraphQL."

HELP_TEXT = f"""
Welcome to { TITLE } \n
{DESCRIPTION}
"""


def click_commands(core_cli, items: list):
    """Collect (Click) Commands"""
    command_sources = [core_cli]
    for active in items:
        if isinstance(active.object, click.core.Group):
            command_sources.append(active.object)
    return click.CommandCollection(name=TITLE, help=HELP_TEXT, sources=command_sources)


def shell_print(text: str, color: str = "green"):
    """Shell Print"""
    return click.secho(f"{ text }", fg=color, bold=True)


def shell_command(list_of_commands: str | list[str]):
    """Execute a list of Shell Commands"""

    processes = []
    if not isinstance(list_of_commands, list):
        list_of_commands = [list_of_commands]
    for cmd in list_of_commands:
        split_cmd = shlex.split(cmd)
        # task = subprocess.Popen(split_cmd, shell=True)
        # processes.append(task)
        with subprocess.Popen(split_cmd, shell=True) as task:
            processes.append(task)
    return [process.wait() for process in processes]
