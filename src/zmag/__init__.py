# -*- coding: utf-8 -*-
"""
**ZMAG** is a powerful tool designed for building **network APIs**.
"""

import logging

from .external import spoc, strawberry
from .network import BackendZMQ as Backend
from .network import DeviceZMQ as Device
from .network import FrontendZMQ as Frontend
from .network.utils import Data

# Logs
logging.basicConfig(format="%(levelname)s    -  %(message)s", level=logging.INFO)


# Server
if spoc and strawberry:
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
        from .framework.components import BaseType, Model, Type, cli
        from .framework.components import graphql as gql
        from .framework.components import graphql_input as input  # pylint: disable=W

        # GraphQL Forms
        from .framework.components.forms import UNSET
        from .framework.components.forms import BaseForm as Input
        from .framework.components.forms import form_cleaner as clean
        from .framework.components.forms import form_field as value
        from .framework.components.objects import dataclass_field as field

        # Framework Core
        from .framework.framework import Framework as App

        # GraphQL Tools
        from .graphql.types import Edge as edge
        from .graphql.types import Error as errors
        from .graphql.types import ErrorMessage as error
        from .graphql.types import Mutation as mutation
        from .graphql.types import page

        # Object Tools
        from .tools import docs

        # Scalars
        ID = strawberry.ID
        json = JSON

    # Ignores When Using Client (ONLY)
    except ImportError:
        pass
    except TypeError:
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
    "clean",
    "input",
    "value",
    # Reponses
    "edge",
    "error",
    "errors",
    "mutation",
    "page",
    # Utils
    "docs",
)
