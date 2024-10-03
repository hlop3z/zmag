# -*- coding: utf-8 -*-
"""
GraphQL Types
"""

# Read the Docs
# https://hlop3z.github.io/zmag/server/graphql/types/

from typing import Annotated, TypeAlias, TypeVar

import zmag

# Forward References
T = TypeVar("T")
Ref: TypeAlias = Annotated[T, zmag.lazy_type(".types")]


# Create your <Types> here.
