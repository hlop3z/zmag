# GraphQL **Types**

The code **must** be placed in a **file** named **`types.py`** or within a **folder** named **`types`** located in the **Application directory**.

---

## Type Tools — [Reference](/{{ url("/api/graphql/#zmag.Type") }})

- **`zmag.Type`** — Base class for defining types.
- **`zmag.Model`** — Base class for defining types that include `_id` and `id`.
- **`zmag.BaseType`** — Base class for abstract types.

!!! note

    Tools used for creating GraphQL `object` types.

---

```python title="types.py"
import zmag


# Create your <types> here.

class Author(zmag.Type):  # zmag.BaseType
    """(Type) Read The Docs"""

    first_name: str
    last_name: str

    @property
    async def full_name(self):
        """Full Name"""
        return f"{self.first_name or ""} {self.last_name or ""}"


class Book(zmag.Model):
    """(Type) Read The Docs"""

    title: str
    author: Author
```
