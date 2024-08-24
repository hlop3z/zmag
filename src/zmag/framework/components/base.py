# -*- coding: utf-8 -*-
"""
Components Base
"""

from ...external import spoc

components = spoc.Components(
    # Click
    "command",
    # ZMQ
    "pub",
    "push",
    # GraphQL
    "graphql",
    "input",
    "type",
)
