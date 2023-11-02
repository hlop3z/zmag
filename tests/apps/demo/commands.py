# -*- coding: utf-8 -*-
"""
    { Commands }
"""

import zmag
import click


# Init Click Group
@zmag.cli
def cli():
    """Click (CLI) Group"""


# Create <Commands> here.
@cli.command()
def hello_world():
    """Demo CLI Function"""

    click.echo("Hello World")
