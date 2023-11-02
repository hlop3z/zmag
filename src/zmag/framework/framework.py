# -*- coding: utf-8 -*-
"""{ Core } Read The Docs"""

import spoc
import dbcontroller as dbc
from ..ariadne import create_graphql_app
from .commands.shell import click_commands
from .commands.cli import cli

PLUGINS = ["schema", "manager", "commands"]


@spoc.singleton
class Framework:
    """Framework"""

    def keys(self):
        """Finally: Collect { Keys }"""
        return sorted(
            [
                x
                for x in dir(self)
                if not x.startswith("_") and x not in ["init", "keys"]
            ]
        )

    def init(
        self,
    ):
        """Class __init__ Replacement"""
        framework = spoc.App(plugins=PLUGINS)  #

        # Core
        self.base_dir = framework.base_dir
        self.mode = framework.mode

        # Settings
        self.env = framework.config["env"]
        self.pyproject = framework.config["pyproject"]
        self.spoc = framework.config["spoc"].get("spoc")
        self.settings = framework.settings

        # Project
        self.component = framework.component  #
        self.extras = framework.extras  #
        self.zmq = None

        # Command-Line-Interface
        self.cli = click_commands(cli, framework.component.commands.values())

        # Database
        database = self.spoc.get("database")
        db_engine = database.get("engine", "")
        db_config = database.get("config")

        db_admin = None
        match db_engine:
            case "sql":
                db_admin = dbc.Controller(sql=db_config)
            case "mongo":
                db_admin = dbc.Controller(mongo=db_config)

        # Set Self Database
        self.database = db_admin

        # Ariadne Application
        json_models = []
        class_models = []
        for item in self.component.schema.values():
            json_models.extend(item.object.types)

        for item in self.component.manager.values():
            class_models.append(item.object)

        # Max (Depth & Limit)
        graphql_config = self.spoc.get("graphql", {})

        API = create_graphql_app(
            self.database,
            json_models=json_models,
            class_models=class_models,
            max_depth=graphql_config.get("max_depth", 4),
            max_limit=graphql_config.get("max_limit", 10),
        )
        self.api = API
        self.execute = API.execute
        self.graphql_schema = API.graphql
