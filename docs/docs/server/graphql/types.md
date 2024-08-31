# GraphQL **Types**

The code **must** be placed in a **file** named **`types.py`** or within a **folder** named **`types`** located in the **Application directory**.

---

## Type Tools — [Reference](/{{ url("/api/graphql/#zmag.Type") }})

- **`zmag.Type`** — Base class for defining types.
- **`zmag.Model`** — Base class for defining types that include `_id` and `id`.
- **`zmag.BaseType`** — Base class for abstract types.

!!! tip

    Tools used for creating GraphQL `OBJECT` types.

---

## Using **`zmag.Type`**

```python title="types.py"
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

## Examples

---

### Type Example

Creating the `Author` class using `zmag.Type`.

```python
@dataclass
class Author(zmag.Type): ...
```

### Model Example

Creating the `Author` class using `zmag.Model`.

```python
@dataclass
class Author(zmag.Model): ...
```

### Property Example

Creating a computed field `full_name` in the `Author` class with a property method.

```python
from dataclasses import dataclass

import zmag

@dataclass
class Author(zmag.Type):
    first_name: str
    last_name: str

    @property
    async def full_name(self):
        """Full Name"""
        return f"{self.first_name or ''} {self.last_name or ''}"
```
