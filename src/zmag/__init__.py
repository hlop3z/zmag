# -*- coding: utf-8 -*-
"""
ZMAG
"""

import logging

from .external import spoc, strawberry
from .network import FrontendZMQ as Frontend
from .network import BackendZMQ as Backend
from .network import DeviceZMQ as Device
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

        from .framework.components import pub  # ZMQ
        from .framework.components import push  # ZMQ
        from .framework.components import Model
        from .framework.components import Type as type  # pylint: disable=W
        from .framework.components import cli
        from .framework.components import graphql as gql

        # Framework Core
        from .framework.framework import Framework as App
        from .framework.objects import dataclass_field as field

        # GraphQL Forms
        from .graphql.forms import dataclass as form
        from .graphql.forms import form_cleaner as clean
        from .graphql.forms import form_field as value
        from .graphql.forms import graphql_input as input  # pylint: disable=W

        # GraphQL Tools
        from .graphql.types import Edge as edge
        from .graphql.types import Error as errors
        from .graphql.types import ErrorMessage as error
        from .graphql.types import Mutation as mutation
        from .graphql.types import page

        # Object Tools
        from .tools import docs

        # Model
        model = tuple([type, Model])

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
    "settings",
    "App",
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
    "type",
    "model",
    "form",
    # Form Tools
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
