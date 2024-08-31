# -*- coding: utf-8 -*-
"""
**ZMAG** is a powerful tool designed for building **network APIs**.
"""

import logging
import os

from .external import SPOC, STRAWBERRY
from .network import BackendZMQ as Backend
from .network import DeviceZMQ as Device
from .network import FrontendZMQ as Frontend
from .network.base import ConfigSSH
from .network.utils import Data

# Logs
logging.basicConfig(format="%(levelname)s    -  %(message)s", level=logging.INFO)

# Client or Device - Mode
ZMAG_TYPE = os.getenv("ZMAG_TYPE")

# Server
if SPOC and STRAWBERRY and not ZMAG_TYPE:
    try:
        # Strawberry
        # import strawberry

        # Spoc
        from spoc import settings

        # Strawberry
        from strawberry.extensions import SchemaExtension as BaseExtension
        from strawberry.permission import BasePermission
        from strawberry.scalars import JSON
        from strawberry.schema.config import StrawberryConfig as BaseConfig
        from strawberry.types.lazy_type import lazy as lazy_type

        # Components
        from .framework.components import pub  # ZMQ
        from .framework.components import push  # ZMQ
        from .framework.components import BaseType, Input, Model, Type, cli
        from .framework.components import graphql_decorator as gql
        from .framework.components import graphql_input as input  # pylint: disable=W
        from .framework.components.commands import CLI

        # GraphQL Forms
        from .framework.components.forms import UNSET, Form
        from .framework.components.forms import form_field as value
        from .framework.components.forms import value_cleaner as clean
        from .framework.components.objects import dataclass_field as field

        # Framework Core
        from .framework.framework import Framework as App
        from .graphql.inputs import Pagination, Selector

        # GraphQL Tools
        from .graphql.types import Connection as Edge
        from .graphql.types import Error as Errors
        from .graphql.types import ErrorMessage as Error
        from .graphql.types import Mutation, edge, input_error, Record

        # Other Tools
        from .tools.coro import coro
        from .tools.generic import docs

        # Scalars
        ID = STRAWBERRY.ID
        json = JSON

    # Ignores When Using Client (ONLY)
    finally:
        pass

__all__ = (
    # Spoc,
    "App",
    "settings",
    # ZMQ
    "Frontend",
    "Backend",
    "Device",
    "Data",
    "ConfigSSH",
    "pub",
    "push",
    # Strawberry
    "BaseConfig",
    "BaseExtension",
    "BasePermission",
    # Core
    "cli",
    "CLI",
    "gql",
    "field",
    # GraphQL Object Types
    "BaseType",
    "Type",
    "Model",
    "Input",
    "lazy_type",
    # GraphQL Form Tools
    "UNSET",
    "Form",
    "clean",
    "input",
    "value",
    # GraphQL Reponses
    "Edge",
    "Error",
    "Errors",
    "Mutation",
    "Record",
    "edge",
    "input_error",
    # GraphQL Built-in Inputs
    "Selector",
    "Pagination",
    # Utils
    "docs",
    "coro",
)
