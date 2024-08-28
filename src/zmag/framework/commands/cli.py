# -*- coding: utf-8 -*-
"""
Core { Commands }
"""

from ...external import click

if click:
    # Import Commands Here
    from .certificates import gen_keys
    from .run_server import run, device

    @click.group
    def cli():
        "Click (CLI)"

    # Register Commands
    cli.add_command(run)
    cli.add_command(device)
    cli.add_command(gen_keys)
