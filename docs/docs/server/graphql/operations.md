# GraphQL **Operations**

The code **must** be placed in a **file** named **`graphql.py`** or within a **folder** named **`graphql`** located in the **Application directory**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  demo/
    |         `-- graphql.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  demo/
    |         `-- graphql/            --> <Directory> - Your GraphQL in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

=== ":material-file: File"

    ``` python title="graphql.py"
    # -*- coding: utf-8 -*-
    """
    API - GraphQL
    """

    # ZMAG
    import zmag


    # Create your API (GraphQL) here.
    @zmag.gql
    class Graphql:

        class Query:
            ...

        class Mutation:
            ...

    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
    GraphQL - Init
    """

    # Import your <cruds> here.
    from .api import Graphql
    ```

    ``` python title="api.py"
    # -*- coding: utf-8 -*-
    """
    API - GraphQL
    """

    # ZMAG
    import zmag


    # Create your API (GraphQL) here.
    @zmag.gql
    class Graphql:

        class Query:
            ...

        class Mutation:
            ...
    ```

---

## GraphQL `class` Sections

- **`Meta`**
- **`Query`**
- **`Mutation`**

---

## Meta (Optional)

The `Meta` class allows you to customize the behavior and configuration of your GraphQL.

- **`app`** (`str | None`): Specifies the application name or identifier.
- **`model`** (`str | type | None`): Associates the GraphQL operations with a model. This can be a string representing the model name or an actual `type` class.

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
