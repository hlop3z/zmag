# -*- coding: utf-8 -*-
"""
Core { Commands }
"""

import click

from .core_commands import channels, device, runserver, tasks

# Import Commands Here
from .keypair import gen_keys


@click.group()
def cli():
    "Click (CLI)"


# Register Commands
cli.add_command(device)
cli.add_command(runserver)

cli.add_command(gen_keys)

cli.add_command(channels)
cli.add_command(tasks)
