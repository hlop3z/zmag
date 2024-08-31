"""
Commands
"""

# import os
# import pathlib
# import shutil
# import zipfile

import shlex
import subprocess

import click
from click_help_colors import HelpColorsMultiCommand

# from click.termui import _ansi_colors


TITLE = "ZMAG"
DESCRIPTION = "Craft APIs with ZeroMQ and GraphQL."

HELP_TEXT = f"""
Welcome to { TITLE } \n
{DESCRIPTION}
"""


# Custom CommandCollection class for using colored help
class CommandCollection(HelpColorsMultiCommand, click.CommandCollection):
    """Command Collection with HelpColors"""


def click_commands(core_cli, items: list):
    """Collect (Click) Commands"""

    # INIT Command(s) Sources
    command_sources = [core_cli]

    # Collect All Commands
    for active in items:
        if isinstance(active.object, click.core.Group):
            command_sources.append(active.object)
        elif isinstance(active.object, click.core.Command):
            core_cli.add_command(active.object)

    return CommandCollection(
        name=TITLE,
        help=HELP_TEXT,
        sources=command_sources,
        help_headers_color="yellow",
        help_options_color="bright_cyan",
        help_options_custom_colors={"--help": "bright_magenta"},
    )


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
