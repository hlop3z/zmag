# -*- coding: utf-8 -*-
"""
Core { Commands }
"""

import click

# Import Commands Here
from .certificates import gen_keys
from .core_commands import channels, device, runserver


@click.group()
def cli():
    "Click (CLI)"


# Register Commands
cli.add_command(channels)
cli.add_command(device)
cli.add_command(runserver)

cli.add_command(gen_keys)
