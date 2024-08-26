# -*- coding: utf-8 -*-
"""
**ZMAG** is a powerful tool designed for building **network APIs**.
"""

import logging
import os

from .external import spoc, strawberry
from .network import BackendZMQ as Backend
from .network import DeviceZMQ as Device
from .network import FrontendZMQ as Frontend
from .network.utils import Data

# Version
__version__ = "0.0.13"

# Logs
logging.basicConfig(format="%(levelname)s    -  %(message)s", level=logging.INFO)

# Client Mode
ZMAG_CLIENT = os.getenv("ZMAG_CLIENT")

# Server
if spoc and strawberry and not ZMAG_CLIENT:
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

        # Components
        from .framework.components import pub  # ZMQ
        from .framework.components import push  # ZMQ
        from .framework.components import BaseType, Input, Model, Type, cli
        from .framework.components import graphql_decorator as gql
        from .framework.components import graphql_input as input  # pylint: disable=W

        # GraphQL Forms
        from .framework.components.forms import UNSET, Form
        from .framework.components.forms import form_field as value
        from .framework.components.forms import value_cleaner as clean
        from .framework.components.objects import dataclass_field as field

        # Framework Core
        from .framework.framework import Framework as App

        # GraphQL Tools
        from .graphql.types import Edge
        from .graphql.types import Error as Errors
        from .graphql.types import ErrorMessage as Error
        from .graphql.types import Mutation, edge

        # Other Tools
        from .tools.coro import coro
        from .tools.generic import docs

        # Scalars
        ID = strawberry.ID
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
    "pub",
    "push",
    # Strawberry
    "BaseConfig",
    "BaseExtension",
    "BasePermission",
    # Core
    "cli",
    "gql",
    "field",
    # Object Types
    "BaseType",
    "Type",
    "Model",
    "Input",
    # Form Tools
    "UNSET",
    "Form",
    "clean",
    "input",
    "value",
    # Reponses
    "Edge",
    "Error",
    "Errors",
    "Mutation",
    "edge",
    # Utils
    "docs",
    "coro",
)
