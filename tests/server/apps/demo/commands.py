# -*- coding: utf-8 -*-
"""
Commands
"""

import click

import zmag


# Init Click Group
@zmag.cli
def cli():
    """Click (CLI) Group"""


# Create <Commands> here.
@cli.command()
@zmag.coro
async def hello_world():
    """Demo CLI Function"""

    click.echo("Hello World")
