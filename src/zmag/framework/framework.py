# -*- coding: utf-8 -*-
"""
Framework Core
"""

from types import SimpleNamespace
from typing import Any

from ..external import spoc
from . import handlers
from .commands.cli import cli
from .shell import click_commands

PLUGINS = [
    # Click
    "commands",
    # ZMQ
    "publishers",
    "pushers",
    # GraphQL
    "graphql",
    "types",
    "forms",
]


def get_project_info(framework):
    """Get Name and Version"""
    pyproject = framework.config.get("pyproject", {}).get("project", {})
    spoc_info = framework.config.get("spoc", {}).get("spoc")

    # Pyproject
    name = pyproject.get("name")
    version = pyproject.get("version")

    # Spoc
    if not name:
        name = spoc_info.get("name")
    if not version:
        version = spoc_info.get("version")

    return {"name": name, "version": version}


if spoc:

    class Framework(spoc.Base):
        """Framework
        - base_dir
        - cli
        - context
        - debug
        - env
        - events
        - graphql
        - graphql_settings
        - info
        - mode
        - publishers
        - pushers
        - pyproject
        - schema
        - settings
        - spoc
        - zmq
        """

        base_dir: Any
        cli: Any
        context: Any
        debug: Any
        env: Any
        events: Any
        graphql: Any
        graphql_settings: Any
        info: Any
        mode: Any
        publishers: Any
        pushers: Any
        pyproject: Any
        schema: Any
        settings: Any
        spoc: Any
        zmq: Any

        def keys(self):
            """Collect { Keys }"""
            return sorted(
                [
                    x
                    for x in dir(self)
                    if not x.startswith("_") and x not in ["init", "keys"]
                ]
            )

        def init(self):
            """Class __init__ Replacement"""
            framework: Any = spoc.init(plugins=PLUGINS)  #

            # Core
            self.base_dir = spoc.settings.BASE_DIR
            self.mode = spoc.settings.MODE

            # Debug
            self.debug = spoc.settings.DEBUG

            # Settings
            self.env = spoc.settings.ENV
            self.spoc = spoc.settings.SPOC
            self.settings = spoc.settings
            self.pyproject = spoc.settings.CONFIG.get("pyproject", {})
            self.graphql_settings = spoc.settings.SPOC.get("graphql", {})

            # Project
            # self.component = framework.components
            # self.extras = framework.extras
            self.info = SimpleNamespace(**get_project_info(framework))
            self.events = SimpleNamespace(
                startup=framework.extras.get("on_startup", []),
                shutdown=framework.extras.get("on_shutdown", []),
            )

            # ZMQ
            self.zmq = None
            self.pushers = handlers.pushers(framework.components.pushers.values())
            self.publishers = handlers.publishers(
                framework.components.publishers.values()
            )

            # Command-Line-Interface
            self.cli = click_commands(cli, framework.components.commands.values())

            # GraphQL { Query & Mutation }
            self.graphql = handlers.graphql(
                schemas=framework.components.graphql.values(),
                permissions=framework.extras.get("permissions", []),
            )

            # GraphQL Schema
            introspection = spoc.settings.DEBUG or self.graphql_settings.get(
                "introspection", False
            )
            self.schema = self.graphql.schema(
                introspection=introspection,
                max_depth=self.graphql_settings.get("max_depth", 4),
                extensions=framework.extras.get("extensions", []),
            )

            # Context
            self.context = SimpleNamespace(schema=self.schema)

            # raise ValueError("DON'T START")
