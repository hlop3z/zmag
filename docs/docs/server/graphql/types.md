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
import zmag

class Author(zmag.Type):
    name: str

class Book(zmag.Type):
    title: str
    author: Author
```

---

## Examples

---

### Type Example

Creating the `Author` class using `zmag.Type`.

```python
import zmag

class Author(zmag.Type): ...
```

### Model Example

Creating the `Author` class using `zmag.Model`.

```python
import zmag

class Author(zmag.Model): ...
```

### Property Example

Creating a computed field `full_name` in the `Author` class with a property method.

```python
import zmag

class Author(zmag.Type):
    first_name: str
    last_name: str

    @property
    async def full_name(self):
        """Full Name"""
        return f"{self.first_name or ''} {self.last_name or ''}"
```
