# -*- coding: utf-8 -*-
"""
Commands
"""

from typing import Literal

import click

import zmag

click.Option


# Init Click Group
@zmag.cli
def cli():
    """Click (CLI) Group"""


@zmag.cli(group=True)
def database():
    """Click (CLI) Group"""


# Create <Commands> here.
@database.command()
@zmag.coro
async def hello_world_group():
    """Demo CLI Function"""

    zmag.cli.echo("Hello World Group")


@cli.command()
@zmag.cli.argument("demo", type=zmag.cli.range(1, 5), help="my custom help")
@zmag.cli.option("--debug", help="my custom help")
@zmag.coro
async def hello_world(demo: int | None, debug: Literal["one", "two"] | None = None):
    """Demo CLI Function"""

    # print(type(debug))
    zmag.cli.echo(f"Hello World CLI { debug } | { demo }")


cli.add_command(database)
