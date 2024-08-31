# -*- coding: utf-8 -*-
"""
Components Base
"""

from ...external import SPOC

components = SPOC.Components(
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
