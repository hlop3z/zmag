"""
    Commands
"""

import os
import pathlib
import shlex
import shutil
import subprocess
import zipfile


import click


TITLE = "Zmag"
DESCRIPTION = "Craft APIs for Databases, with ZeroMQ and GraphQL."

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


def shell_command(list_of_commands: list[str]):
    """Shell Commands"""
    processes = []
    if not isinstance(list_of_commands, list):
        list_of_commands = [list_of_commands]
    for cmd in list_of_commands:
        __code = shlex.split(cmd)
        task = subprocess.Popen(__code, shell=True)
        processes.append(task)
    return [process.wait() for process in processes]


CORE_PATH = pathlib.Path(__file__).parents[2] / "scripts"
TEMPORARY_DIR = CORE_PATH / "tmp"
TEMPLATES_DIR = CORE_PATH / "templates"


def path_delete(dir_path):
    """Delete Path"""
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


def unzip_base(source, destination):
    """Unzip Base"""
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(destination)


def unzip(source: str, destination: str):
    """Unzip Method"""
    source = TEMPLATES_DIR / source
    file_name = source.name
    file_name = file_name.replace(".zip", "")
    unzip_base(source, TEMPORARY_DIR)
    shutil.move(TEMPORARY_DIR / file_name, destination)


def zip(zip_path, source_path):
    """Zip Method"""

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
                )

    with zipfile.ZipFile(f"{str(zip_path)}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipdir(source_path, zipf)
