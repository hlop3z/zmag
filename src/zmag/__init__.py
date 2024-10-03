# -*- coding: utf-8 -*-
"""
**ZMAG** is a powerful tool designed for building **network APIs**.
"""

import datetime as dt
import decimal as dec
import logging
import os
import sys
from typing import Any, TypeAlias
from uuid import UUID as uuid

# Generic Tools
from .external import SPOC, STRAWBERRY
from .network import BackendZMQ as Backend
from .network import DeviceZMQ as Device
from .network import FrontendZMQ as Frontend
from .network.base import ConfigSSH
from .network.keypair import keypair
from .network.utils import Data

# Other Tools
from .tools.coro import coro
from .tools.datetime import Date
from .tools.generic import docs

# Logs
logging.basicConfig(
    format="%(levelname)s    -  %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)

# Client or Device - Mode
ZMAG_TYPE = os.getenv("ZMAG_TYPE")

# Server
if SPOC and STRAWBERRY and not ZMAG_TYPE:
    try:
        # Strawberry
        # import strawberry

        # Spoc
        from spoc import settings
        from strawberry import enum

        # Strawberry
        from strawberry.extensions import SchemaExtension as BaseExtension
        from strawberry.permission import BasePermission
        from strawberry.scalars import JSON as STRAWBERRY_JSON
        from strawberry.schema.config import StrawberryConfig as BaseConfig
        from strawberry.types import Info as InfoGraphql
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

        # GraphQL Tools
        from .graphql.inputs import GenericPagination as Pagination
        from .graphql.inputs import GenericSelector as Selector
        from .graphql.types import Connection as BaseEdge
        from .graphql.types import Error as Errors
        from .graphql.types import ErrorMessage as Error
        from .graphql.types import GenericEdge as Edge
        from .graphql.types import Mutation, Record, edge, input_error

        # Scalars
        JSON: Any = STRAWBERRY_JSON
        ID: str | int = STRAWBERRY.ID
        id: TypeAlias = ID  # type: ignore # pylint: disable=W,C
        json: TypeAlias = JSON  # type: ignore # pylint: disable=C

        # Python Scalars
        time = dt.time  # pylint: disable=C
        date = dt.date  # pylint: disable=C
        datetime = dt.datetime  # pylint: disable=C
        decimal = dec.Decimal  # pylint: disable=C

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
    "keypair",
    # Strawberry
    "BaseConfig",
    "BaseExtension",
    "BasePermission",
    "InfoGraphql",
    # Core
    "cli",
    "CLI",
    "gql",
    "field",
    # GraphQL Scalars
    "id",
    "json",
    "time",
    "date",
    "datetime",
    "decimal",
    "uuid",
    # GraphQL Object Types
    "BaseType",
    "Input",
    "Model",
    "Type",
    "enum",
    "lazy_type",
    # GraphQL Form Tools
    "UNSET",
    "Form",
    "clean",
    "input",
    "value",
    # GraphQL Reponses
    "BaseEdge",
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
    "Date",
    "docs",
    "coro",
)
