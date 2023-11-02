# Client
from .client import Client

# Server
try:
    import spoc
except ImportError:
    spoc = None

try:
    import ariadne
except ImportError:
    ariadne = None


try:
    import dbcontroller as dbc

    DBCONTROLLER = True
except ImportError:
    DBCONTROLLER = False

if spoc and ariadne and DBCONTROLLER:
    from dbcontroller import Controller
    from dbcontroller import mongo_id

    from .ariadne import type
    from .ariadne.resource_api import ResourcesAPI
    from .ariadne.query_depth_limiter import QueryDepthLimiter
    from .framework import COMPONENTS
    from .framework import Framework as App
    from .framework.components import schema, cli

    from .server import server, ZMQ

    # Form Value
    value = dbc.form.field
    filters = dbc.form.filters

    # Scalars
    # ID = dbc.ID
    # date = dbc.date
    # datetime = dbc.datetime
    # time = dbc.time
    # decimal = dbc.decimal
    # text = dbc.text
    # time = dbc.time
    # json = dbc.json
