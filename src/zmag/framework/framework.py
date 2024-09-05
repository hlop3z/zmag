# -*- coding: utf-8 -*-
"""
Framework Core
"""

import os
from types import SimpleNamespace
from typing import Any

from ..external import SPOC
from .commands.cli import cli
from .commands.shell import click_commands
from .components import handlers

MODULES = [
    # Click
    "commands",
    # ZMQ
    "publishers",
    "pushers",
    # GraphQL
    "graphql",
    "types",
    "inputs",
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


if SPOC:

    class Framework(SPOC.Base):
        """Framework
        - base_dir
        - cli
        - context
        - debug
        - env
        - events
        - get_channels
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
            framework: Any = SPOC.init(MODULES)
            self._setup_env()

            # Core
            self.base_dir = SPOC.settings.BASE_DIR
            self.mode = SPOC.settings.MODE

            # Debug
            self.debug = SPOC.settings.DEBUG

            # Settings
            self.env = SPOC.settings.ENV
            self.spoc = SPOC.settings.SPOC
            self.settings = SPOC.settings
            self.pyproject = SPOC.settings.CONFIG.get("pyproject", {})
            self.graphql_settings = SPOC.settings.SPOC.get("graphql", {})

            # Project
            # self.component = framework.components
            # self.plugins = framework.plugins
            self.info = SimpleNamespace(**get_project_info(framework))
            self.events = SimpleNamespace(
                startup=framework.plugins.get("on_startup", []),
                shutdown=framework.plugins.get("on_shutdown", []),
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
                permissions=framework.plugins.get("permissions", []),
            )

            self.types = {
                model.name: model.object
                for model in framework.components.types.values()
            }

            # GraphQL Schema
            introspection = SPOC.settings.DEBUG or self.graphql_settings.get(
                "introspection", False
            )
            self.schema = self.graphql.schema(
                introspection=introspection,
                max_depth=self.graphql_settings.get("max_depth", 4),
                extensions=framework.plugins.get("extensions", []),
            )

            # Context
            self.context = SimpleNamespace(schema=self.schema)

        def get_channels(self) -> set[str]:
            """
            ZeroMQ (Pub/Sub) Channels
            """
            all_channels = set()

            for method in self.publishers.values():
                channel = method.info.config.get("channel", "")
                all_channels.add(channel)

            return all_channels

        def get_tasks(self) -> set[str]:
            """
            ZeroMQ (Push/Pull) Tasks
            """
            all_jobs = set()

            for method in self.pushers.values():
                time_in_seconds = method.info.config.get("time", 0)
                all_jobs.add(f"{method.key}(time={time_in_seconds})")

            return all_jobs

        @staticmethod
        def _setup_env():
            # Init `ZMQ` in environment
            if "zmq" not in SPOC.settings.ENV:
                SPOC.settings.ENV["zmq"] = {}
            # Keys
            env_public_key = os.getenv("ZMAG_PUBLIC_KEY")
            env_secret_key = os.getenv("ZMAG_SECRET_KEY")
            env_server_key = os.getenv("ZMAG_SERVER_KEY")
            # Setters
            if env_public_key:
                SPOC.settings.ENV["zmq"]["public_key"] = env_public_key
            if env_secret_key:
                SPOC.settings.ENV["zmq"]["secret_key"] = env_secret_key
            if env_server_key:
                SPOC.settings.ENV["zmq"]["server_key"] = env_server_key
