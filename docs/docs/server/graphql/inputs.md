# GraphQL **Inputs**

The code **must** be placed in a **file** named **`inputs.py`** or within a **folder** named **`inputs`** located in the **Application directory**.

---

## Input Tools — [Reference](/{{ url("/api/graphql/#zmag.Input") }})

- **`zmag.Input`** — Base class for defining inputs.
- **`zmag.input`** — Initializes input group.
- **`zmag.value`** — Configures input field settings.
- **`zmag.clean`** — Defines cleaning functions or rules.
- **`zmag.Form`** — Represents an input response.

!!! tip

    Tools used for creating GraphQL `INPUT` types.

---

## Using **`zmag.Input`** and **`zmag.input`**

```python title="inputs.py"
import zmag

form = zmag.input("Form")

@form
class Create(zmag.Input): ... # FormCreate

@form
class Update(zmag.Input): ... # FormUpdate
```

---

## Examples

---

### **Required** Field

A required field with no default value; the field must be filled.

```python
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    x: str = zmag.value(required=True)
```

---

### Dynamic **Default** Value

A field with a default value, optionally using a function for initialization.

```python
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Dynamic Default Value"""

    y: str = zmag.value(default="Some Value")
    # OR
    y: str = zmag.value(default=lambda: "Some Value")
```

---

### **Deprecated** Field

A deprecated field, indicating it should no longer be used.

```python
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Deprecated Field"""

    z: str = zmag.value(deprecation_reason="This field is deprecated.")
```

---

### Complex Field with **Validation** and **Cleaning**

A complex field setup demonstrating validation, cleaning, and transformation of input data.

```python
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Complex Field Setup"""

    email: str = zmag.value(
        regex={
            # Regex pattern for email validation.
            r"[\w\.-]+@[\w\.-]+": "Invalid email address"
        },
        rules=[
            # Custom validation rule for the field.
            (lambda v: v.startswith("demo") or "Invalid input")
        ],
        clean=zmag.clean(
            regex=[
                # Replace text in the cleaning phase.
                (r"^hello", "hola"),
                (r"com", "api"),
            ],
            rules=[
                # Transform the value after applying regex replacements.
                (lambda v: v.upper())
            ],
        ),
    )
```

## Example **Usage**

The built-in `input: Form` **attribute** provides flexible access to the input data, allowing you to manipulate and retrieve it in various formats.

```python title="graphql.py"
@zmag.gql
class Graphql:
    ...

    class Mutation:
        async def create(self, form: MyForm | None) -> None:
            if form and form.input.is_valid:
                print(form.input)
                print(form.input.clean())
                print(form.input.dict(True))
            return None
```
