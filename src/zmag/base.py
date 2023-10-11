# -*- coding: utf-8 -*-
"""{ Module } Read The Docs"""
from .spoc_admin import spoc

if spoc:
    from strawberry.permission import BasePermission

    # FrameWork
    from .framework import Framework as App
    from .components import graphql as gql
    from .components import cli
    from .components import forms
    from .server import ZMQ

    # GraphQL Tools
    from .graphql import edges, error, errors, mutation, page, query

    # GraphQL Premade User-Inputs
    from .tools import Item as item
    from .tools import Pagination as pagination
    from .tools import coro, doc

    # Framework Wrappers
    base_dir = spoc.base_dir
    config = spoc.config
    mode = spoc.mode
    project = spoc.project
    settings = spoc.settings

    # Tools
    component = spoc.component

    try:
        import dbcontroller as dbc
        from dbcontroller.forms import ISNULL

        if hasattr(settings, "DATABASES"):
            config_sql = settings.DATABASES.get("sql")
            config_mongo = settings.DATABASES.get("mongo")
            default_sql = config_sql.get("default")
            default_mongo = config_mongo.get("default")
            if default_sql:
                sql = dbc.Controller(sql=default_sql)
            if default_mongo:
                mongo = dbc.Controller(mongo=default_mongo)

        # Types
        type = dbc.type

        # Forms
        input = dbc.form.graphql
        value = dbc.form.field

        # Value Tool
        filters = dbc.form.filters

        # Types Tool (DBController)
        field = dbc.field
        manager = dbc.manager

        # Scalars
        ID = dbc.ID
        date = dbc.date
        datetime = dbc.datetime
        time = dbc.time
        decimal = dbc.decimal
        text = dbc.text
        time = dbc.time
        json = dbc.json

        # Tester
        Date = dbc.Date

    except ImportError:
        import strawberry
        from strawberry.scalars import JSON

        # Types
        type = strawberry.type
        input = strawberry.input
        ID = strawberry.ID
        json = JSON
