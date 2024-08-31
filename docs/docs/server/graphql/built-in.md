
# Extending GraphQL **Operations**

!!! tip

    Utilize these tools to effectively create and manage GraphQL operations.

---

## Mutation Tools — [Reference](/{{ url("/api/graphql/#zmag.Mutation") }})

- **`zmag.Mutation`** — Represents a GraphQL mutation response, handling the outcome of mutation operations.
- **`zmag.Error`** — A structured format for GraphQL error messages to be used in error responses.
- **`zmag.Errors`** — A comprehensive response object for handling multiple GraphQL errors.
- **`zmag.input_error`** — A simplified error handler for mutation errors.

---

## Query Tools — [Reference](/{{ url("/api/graphql/#zmag.Edge") }})

- **`zmag.Record`** — A utility for returning either a `single` object or a `list` of objects, depending on the query response, making it flexible for various use cases.
- **`zmag.Edge`** — Optimizes data retrieval by defining edges in GraphQL queries, allowing for more structured and efficient querying.
- **`zmag.edge`** — A utility for easily creating and managing edges in GraphQL queries, simplifying the setup of relationships between data nodes.

---

## Input Tools — [Reference](/{{ url("/api/graphql/#zmag.Pagination") }})

- **`zmag.Pagination`** — An input type designed to manage pagination, allowing efficient navigation and retrieval of database records.
- **`zmag.Selector`** — A tool for selecting specific database records, enabling targeted data manipulation.

---

## Examples

---

=== "inputs.py"

    ```python
    import zmag

    Book = zmag.input("Book")

    # Create your <input> here.
    @Book
    class Create(zmag.Input):
        title: str    
    ```

=== "types.py"

    ```python
    from dataclasses import dataclass
    from typing import Annotated, TypeAlias, TypeVar

    import zmag

    # ForwardRef
    T = TypeVar("T")
    Ref: TypeAlias = Annotated[T, zmag.lazy_type(".types")]

    # Create your <types> here.
    @dataclass
    class Book(zmag.Type):
        title: str | None = None
        author: Ref["Author"] | None = None


    @dataclass
    class Author(zmag.Type):
        name: str | None = None
        books: list[Book] | None = None
    ```

---

Here's an improved version of your documentation with more clarity and detail:

---

### **Mutation Example**

This example demonstrates how to use `zmag.Mutation`, `zmag.Errors`, and `zmag.Error` to handle mutations in GraphQL. We will also utilize the previously defined `types` and `inputs`.

```python title="graphql.py"
import zmag
from . import inputs, types

@zmag.gql
class Graphql:
    """Books API"""

    class Meta:
        app = None
        model = types.Book

    class Mutation:
        async def create(self, form: inputs.Create) -> zmag.Mutation[types.Book]:
            # Check if the input is not valid
            if not form.input.is_valid:
                return zmag.Mutation(
                    error=zmag.Errors(
                        messages=[zmag.Error(**e) for e in form.input.errors],
                    ),
                )

            # Process valid input
            data = form.input.dict()
            return zmag.Mutation(
                item=types.Book(
                    title=data.get("title"),
                    author=types.Author(name="Michael Crichton"),
                ),
            )
```

#### Example Usage in GraphQL

```graphql
mutation MyMutation {
  bookCreate(form: {title: "Jurassic Park"}) {
    # On success
    item {
      title
      author {
        name
      }
    }
    # On error
    error {
      messages {
        field
        type
        text
      }
    }
  }
}
```

---

### **Simplified Error Handling Example**

To simplify error handling, you can use the built-in `zmag.input_error` wrapper. This example shows how to streamline error responses when input validation fails.

```python
import zmag

async def create(...):
    # Check if the input is not valid
    if not form.input.is_valid:
        return zmag.input_error(form.input.errors)

    # Continue with valid input processing
    ...
```

---
