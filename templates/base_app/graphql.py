# -*- coding: utf-8 -*-
"""
GraphQL API
"""

# Read the Docs
# https://hlop3z.github.io/zmag/server/graphql/operations/

import zmag

from . import inputs, types


# Create <GraphQL> operations here.
@zmag.gql
class Graphql:
    """CRUD"""

    class Meta:
        app = None
        model = None

    class Query: ...

    class Mutation: ...
