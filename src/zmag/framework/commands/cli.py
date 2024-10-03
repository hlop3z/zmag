# -*- coding: utf-8 -*-
"""
Core { Commands }
"""

import click

# Import Commands Here
from .core_commands import channels, runserver, tasks
from .keypair import gen_keys
from .start_app import start_app


@click.group()
def cli():
    "Click (CLI)"


# Register Commands
# cli.add_command(device)
cli.add_command(runserver)

cli.add_command(gen_keys)

cli.add_command(channels)
cli.add_command(tasks)

cli.add_command(start_app)
