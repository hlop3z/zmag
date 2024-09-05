
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
- **`zmag.BaseEdge`** — Base `edge` that allows defining the `computed` field instead of a generic `JSON`.
- **`zmag.Edge`** — Optimizes data retrieval by defining edges in GraphQL queries and included a generic `JSON` based `computed` field.
- **`zmag.edge`** — A utility for returning edges in GraphQL queries

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

Example Usage in GraphQL

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

### **Mutation Simplified Error Example**

To simplify error handling, you can use the built-in `zmag.input_error` tool. This example shows how to streamline error responses when input validation fails.

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

### **Query `Record` Example**

This example demonstrates how to use `zmag.Record`.

```python
... # Graphql
... # Meta

class Query:
    async def one_record(self) -> zmag.Record[types.Book]:
        return zmag.Record(
            item=types.Book(title="The Great Gatsby"), 
            is_many=False
        )

    async def many_records(self) -> zmag.Record[types.Book]:
        return zmag.Record(
            items=[types.Book(title="The Great Gatsby")], 
            is_many=True
        )
```

Example Usage in GraphQL

Usage with `item`

```graphql
query MyQuery {
  bookOneRecord {
    isMany
    item {
      title
    }
  }
}
```

Example Usage in GraphQL

Usage with `items`

```graphql
query MyQuery {
  bookManyRecords {
    isMany
    items {
      title
    }
  }
}
```

---

### **Query `BaseEdge` Example**

This example demonstrates how to use `zmag.BaseEdge` to connect edges with a predefined computed `Type`. The `BaseEdge` is utilized when the edge requires a specific computed type to be associated with it, allowing for more structured data retrieval.

```python
@dataclass
class Computed(zmag.Type):
    total_views: int | None = None
```

```python
# GraphQL query definition
class Query:
    async def many_records(self) -> zmag.BaseEdge[types.Book, types.Computed]:
        # Implementation logic here
        ...
```

---

### **Query `Edge` Example**

This example shows how to use `zmag.Edge`, a more generic type of edge. Here, the computed value is stored in a JSON format, providing flexibility in what data is returned with each edge.

```python
# GraphQL query definition
class Query:
    async def many_records(self) -> zmag.Edge[types.Book]:
        # Implementation logic here
        ...
```

---

### **Query `Pagination` Example**

This example illustrates how to implement `zmag.Pagination` to handle paginated queries. You can configure the **`items_per_page`** setting through a [configuration file](/{{ url("/server/config/settings/#spoctoml") }}), which sets the maximum `limit` a user can request, ensuring efficient data retrieval and performance.

```python
# GraphQL query definition
class Query:
    async def many_records(self, pagination: zmag.Pagination) -> zmag.JSON:
        data = pagination.input.data
        return {
            "page": data.page,
            "limit": data.limit,
            "sort_by": data.sort_by,
        }
```

---

### **Query `Selector` Example**

This example demonstrates the use of `zmag.Selector` for selecting specific records. The `Selector` enables precise querying by allowing users to specify which records to retrieve based on provided `id` or `ids`.

```python
# GraphQL query definition
class Query:
    async def one_record(self, select: zmag.Selector) -> str:
        return select.input.data.id

    async def many_records(self, select: zmag.Selector) -> list[str]:
        return select.input.data.ids
```

**Example Usage in GraphQL with a Single Item:**

```graphql
query MyQuery {
  bookOneRecord(select: {id: 1})
}
```

**Example Usage in GraphQL with Multiple Items:**

```graphql
query MyQuery {
  bookManyRecords(select: {ids: [1, 2, 3]})
}
```
