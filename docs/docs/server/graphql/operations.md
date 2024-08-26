# GraphQL **Operations**

The code **must** be placed in a **file** named **`graphql.py`** or within a **folder** named **`graphql`** located in the **Application directory**.

```python title="graphql.py"
import zmag

# Create your API (GraphQL) here.
@zmag.gql
class Graphql:
    class Meta: ...
    class Query: ...
    class Mutation: ...
```

---

## Operations Tools — [Reference](/{{ url("/api/graphql/#zmag.gql") }})

- **`Meta`**
- **`Query`**
- **`Mutation`**

---

## Meta (Optional)

The `Meta` class can be used to customize the naming and behavior of these GraphQL operations.

- **`app`** (`str | bool | None`): Specifies the application name or identifier.
- **`model`** (`str | type | None`): Associates the GraphQL operations with a model. This can be a string representing the model name or an actual `type` class.

---

## Examples

---

### Without `Meta` (**default**)

When the `Meta` class is not used:

```python
@zmag.gql
class Graphql:
    async def detail(self) -> str:
        return "Detail"
```

**GraphQL Field Name:**

```py
demoDetail
```

**Explanation:** The GraphQL field name is automatically generated based on the **method** name `detail` and **package/application** name `demo`.

---

### With `model`

When the `Meta` class specifies a `model`:

```python
from . import types

@zmag.gql
class Graphql:
    class Meta:
        model = types.Book
```

**GraphQL Field Name:**

```py
demoBookDetail
```

**Explanation:** The GraphQL field name is prefixed with the model name (`Book`), resulting in `demoBookDetail`.

---

### With `app` Set to `None`

When the `Meta` class specifies `app` as `None`:

```python
@zmag.gql
class Graphql:
    class Meta:
        app = None
        ...
```

**GraphQL Field Name:**

```py
detail
```

**Explanation:** The `app` value is ignored, so the GraphQL field name is based directly on the method name `detail`.

### With custom `app`

```python
@zmag.gql
class Graphql:
    class Meta:
        app = "custom"
        ...
```

**GraphQL Field Name:**

```py
customDetail
```

**Explanation:** The GraphQL field name is automatically generated based on the **method** name `detail` and provided **app** name `custom`.

### Full Example

```python
import zmag

@zmag.gql
class Graphql:

    class Meta:
        app = True
        model = "Book"

    class Query:
        async def detail(self) -> str:
            return "Detail (Query)"

    class Mutation:
        async def create(self) -> str::
            return "Create (Mutation)"
```
