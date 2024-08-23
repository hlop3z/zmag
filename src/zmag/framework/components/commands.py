# -*- coding: utf-8 -*-
"""
Click (commands)
"""

import functools
import typing

from ...external import click
from .base import components


# Command-Line Interface
def cli(obj: typing.Any = None, *, group: bool = False) -> typing.Any:
    """Click { CLI } Creator"""
    if obj is None:
        return functools.partial(cli, group=group)
    # Real Wrapper
    obj = click.group(obj)  # type: ignore
    if not group:
        components.register("command", obj)
    return obj
