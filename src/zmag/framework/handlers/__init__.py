# -*- coding: utf-8 -*-
"""
{ Framework Handlers }
"""

from .graphql.base import graphql
from .utils import generic_collector


def forms(models: list):
    """Collect (GraphQL) Return-Types"""
    return generic_collector("form", models)


def types(models: list):
    """Collect (GraphQL) Input-Forms"""
    return generic_collector("type", models)


def pushers(models: list):
    """Collect (ZMQ) Pushers"""
    return generic_collector("push", models, generics=True)


def publishers(models: list):
    """Collect (ZMQ) Publishers"""
    return generic_collector("pub", models, generics=True)


__all__ = (
    "graphql",
    "types",
    "forms",
    "publishers",
    "pushers",
)
