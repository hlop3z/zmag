"""
    Start A New Fastberry Project
"""

import os.path

import click

from .shell import shell_print, unzip
import spoc


@click.command()
@click.argument(
    "app_name",
    type=str,
    nargs=1,
)
def start_app(app_name):
    """Zmag Start Application."""
    # Get Path(s)
    apps_dir = spoc.base_dir / "apps"
    the_dir = apps_dir / app_name

    # Create Path(s)
    apps_dir.mkdir(parents=True, exist_ok=True)

    # Check Path(s)
    if os.path.isdir(the_dir):
        shell_print(
            f"""* Error: "{{ { app_name } }}" App Already Exists!""", color="red"
        )
    else:
        shell_print(
            f"""* Starting App: "{{ { app_name } }}" . . .""",
        )
        # unzip("base_app.zip", the_dir)
        unzip("app-template.zip", the_dir)
