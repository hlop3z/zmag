# -*- coding: utf-8 -*-
"""
GraphQL API
"""

import zmag

from . import inputs, types


@zmag.gql
class Graphql:
    """Books API"""

    class Meta:
        app = None
        model = types.Book

    class Query:
        async def test(self, select: zmag.Selector) -> zmag.json:
            return {
                "page": 1,
                "limit": 1,
                "sort_by": 1,
            }

        async def list(
            self,
            pagination: zmag.Pagination,
        ) -> zmag.BaseEdge[types.Book, types.Book]:
            """Read the Docs"""
            # print(pagination.input.data)
            return zmag.edge(
                edges=[
                    types.Book(
                        _id=1,
                        id="1",
                        title="The Great Gatsby",
                        author=types.Author(
                            first_name="F. Scott", last_name="Fitzgerald"
                        ),
                        time=zmag.Date.time(),
                        date=zmag.Date.date(),
                        datetime=zmag.Date.datetime(),
                    ),
                ]
            )

    class Mutation:
        async def create(self, form: inputs.Create) -> zmag.Mutation[types.Book]:
            """Read the Docs"""
            print(form)

            # Not Valid
            if not form.input.is_valid:
                return zmag.input_error(form.input.errors)

            # Is Valid
            data = form.input.dict()
            return zmag.Mutation(
                item=types.Book(
                    title=data.get("title"),
                    author=types.Author(first_name="Michael", last_name="Crichton"),
                ),
            )


'''
# Create your API (GraphQL) here.
@zmag.gql
class Graphql:
    """Demo Api"""

    class Meta:
        """GQL-Class Metadata"""

        app = True
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

        async def create(self, form: inputs.Create | None) -> zmag.Mutation[types.Book]:
            """Read the Docs"""
            if form:
                # form.input.dict(True)
                # form.input.clean()
                print(form.input.data)
                print(form.input.dict(True))
                print(form.input.clean())
            return zmag.Mutation()
'''
