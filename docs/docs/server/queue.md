# `Queue`

In this guide, you'll learn how to implement `Request/Response` operations, with GraphQL.

## `GraphQL` Operations

Must be inside a file named `graphql.py`

This is the most common and default way to use `zmag`. This is to create a `Request/Response` pattern also known as `client/server` model.

### Example

```python title="types.py"
class Book:
    title: str
    author: "Author"

class Author:
    name: str
    books: list[Book]
```

```python title="graphql.py"
import zmag

from . import inputs, types

@zmag.gql
class Graphql:

    class Meta:
        app = None
        model = types.Book

    class Query:
        async def items(self) -> list[types.Book] :
            return [
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                ),
            ]

    class Mutation:
        async def create(self) -> str::
            return "Create (Mutation)"
```
