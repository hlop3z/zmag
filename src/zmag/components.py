"""
    Components
"""
import functools

import click
from .spoc_admin import spoc

try:
    import dbcontroller as dbc
except:
    dbc = None

COMPONENT = {}
COMPONENT["graphql"] = {"engine": "strawberry-graphql", "type": "schema"}
COMPONENT["commands"] = {"engine": "click", "type": "group"}
COMPONENT["form-admin"] = {"engine": "graphql-form-admin", "type": "form"}


# GraphQL Class @Decorator
def graphql(
    cls: object = None,
):
    """Strawberry { GraphQL } Creator"""
    spoc.component(cls, metadata=COMPONENT["graphql"])
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
        spoc.component(cls, metadata=COMPONENT["commands"])
    return cls


def get_attributes(obj):
    return [attr for attr in dir(obj) if not attr.startswith("__")]


def forms(
    cls: object = None,
):
    """{ GraphQL } Forms"""
    if dbc:
        class_name = cls.__name__.lower()
        for form in get_attributes(cls):
            current = getattr(cls, form)
            updated = dbc.form.graphql(f"form_{class_name}_")(current)
            setattr(cls, form, updated)
    spoc.component(cls, metadata=COMPONENT["form-admin"])
    return cls
