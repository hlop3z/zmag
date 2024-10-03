"""
Create A New App
"""

import os.path

import click
from spoc import settings

from .shell import shell_print
from .unzipper import unzip


@click.command()
@click.argument("app_name", type=str, nargs=1)
def start_app(app_name):
    """Creates a ZMAG App Directory."""
    # Get Path(s)
    apps_dir = settings.BASE_DIR / "apps"
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
        unzip("base_app.zip", the_dir)
