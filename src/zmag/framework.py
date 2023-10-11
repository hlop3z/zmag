# -*- coding: utf-8 -*-
"""{ Core } Read The Docs"""

from .spoc_admin import spoc
from . import handlers

PLUGINS = ["types", "forms", "graphql", "commands"]


@spoc.singleton
class Framework:
    """Framework"""

    def init(
        self,
    ):
        """Class __init__ Replacement"""
        framework = spoc.App(plugins=PLUGINS)  #

        # Self { Definitions }
        core_toml = framework.config["spoc"].get("spoc", {})

        self.settings = framework.settings
        self.is_production = core_toml.get("mode", "development") == "production"

        # Core
        self.base_dir = framework.base_dir
        self.mode = framework.mode

        # Settings
        self.env = framework.config["env"]
        self.pyproject = framework.config["pyproject"]
        self.spoc = framework.config["spoc"]
        self.settings = framework.settings

        # Project
        self.component = framework.component
        self.extras = framework.extras

        # Create API
        self.zmq = None
        self.core = framework
        self.graphql = None
        self.toml = core_toml

        # Pagination : print(self.pagination(page=0, limit=500))
        self.pagination = handlers.pagination(core_toml)

        if framework.component:
            # GraphQL { Types }
            self.types = handlers.types(framework.component.types.values())

            # GraphQL { Forms }
            self.forms = handlers.forms(framework.component.forms.values())

            # GraphQL { Query & Mutation }
            self.graphql = handlers.graphql(
                schemas=framework.component.graphql.values(),
                permissions=self.extras.get("permissions", []),
            )

            # Command-Line-Interface
            self.cli = handlers.commands(framework.component.commands.values())

        # List All Tools
        self.keys = [
            "base_dir",
            "mode",
            "env",
            "pyproject",
            "spoc",
            "settings",
            "component",
            "extras",
        ]
