# -*- coding: utf-8 -*-
"""
GraphQL API
"""

import zmag

from . import inputs, types


# Create your API (GraphQL) here.
@zmag.gql
class Graphql:
    """Demo Api"""

    class Meta:
        """GQL-Class Metadata"""

        # app = None
        model = types.Book

    class Query:
        """Query"""

        async def detail(self) -> str:
            """Read the Docs"""
            # print(info)
            return "Detail"

        async def list(self) -> list[types.Book | None]:
            """Read the Docs"""
            # print(info)
            return [
                types.Book(
                    _id=1,
                    id="1",
                    title="The Great Gatsby",
                    author=types.Author(
                        first_name="F. Scott",
                        last_name="Fitzgerald",
                    ),
                )
            ]

    class Mutation:
        """Mutation"""

        async def create(self, form: inputs.Create | None) -> zmag.mutation[types.Book]:
            """Read the Docs"""
            if form:
                # form.input.dict(True)
                # form.input.clean()
                print(form.input)
                print(form.input.dict(True))
                print(form.input.clean())
            return zmag.mutation()
