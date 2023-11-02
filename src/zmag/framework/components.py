# -*- coding: utf-8 -*-
"""{ Components } Read The Docs"""
import functools


import click
import spoc

COMPONENTS = {}
COMPONENTS["command"] = {"type": "command"}
COMPONENTS["model"] = {"type": "model"}
COMPONENTS["schema"] = {"type": "schema"}


# Class @Decorator
def schema(
    cls: object = None,
):
    """Component Demo"""
    extra_conf = {}
    spoc.component(cls, config=extra_conf, metadata=COMPONENTS["schema"])
    return cls


# Command-Line Interface
def cli(
    cls: object = None,
    *,
    group: bool = False,
):
    """Click { CLI } Creator"""
    if cls is None:
        return functools.partial(
            cli,
            group=group,
        )
    # Real Wrapper
    cls = click.group(cls)
    if not group:
        spoc.component(cls, metadata=COMPONENTS["command"])
    return cls
