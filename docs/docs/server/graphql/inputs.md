# GraphQL **Inputs**

The code **must** be placed in a **file** named **`inputs.py`** or within a **folder** named **`inputs`** located in the **Application directory**.

```python title="inputs.py"
# -*- coding: utf-8 -*-
"""
GraphQL Inputs
"""

import zmag

form = zmag.input("Form")

@form
class Create(zmag.Input):
    """(Input) Read The Docs"""
    ...

@form
class Update(zmag.Input):
    """(Input) Read The Docs"""
    ...
```

---

## Input Tools

- **`zmag.Input`** — Base class for defining inputs.
- **`zmag.input`** — Initializes input group.
- **`zmag.value`** — Configures input field settings.
- **`zmag.clean`** — Defines cleaning functions or rules.

---

## Args `zmag.value`

| Field                | Description                                        |
| -------------------- | -------------------------------------------------- |
| `required`           | Indicates if the field is mandatory.               |
| `regex`              | Dictionary of regex patterns for validation.       |
| `rules`              | List of custom validation rules.                   |
| `clean`              | Cleaning function or rules for processing input.   |
| `deprecation_reason` | Reason why the field is deprecated, if applicable. |

## Args `zmag.clean`

| Field   | Description                                 |
| ------- | ------------------------------------------- |
| `regex` | List of regex patterns for cleaning values. |
| `rules` | List of custom rules for processing values. |

---

## Examples

---

### Required Field

```python title="inputs_required.py"
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Required Field"""

    # A required field with no default value; the field must be filled.
    x: str = zmag.value(required=True)
```

---

### Dynamic Default Value

```python title="inputs_default.py"
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Dynamic Default Value"""

    # A field with a dynamic default value, optionally using a function for initialization.
    y: str = zmag.value(default="Some Value")
    # OR
    y: str = zmag.value(default=lambda: "Some Value")
```

---

### Deprecated Field

```python title="inputs_deprecated.py"
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Deprecated Field"""

    # A deprecated field, indicating it should no longer be used.
    z: str = zmag.value(deprecation_reason="This field is deprecated.")
```

---

### Complex Field with Validation and Cleaning

```python title="inputs_complex.py"
import zmag

Author = zmag.input("Author")

@Author
class MyForm(zmag.Input):
    """GraphQL Form with Complex Field Setup"""

    # A complex field setup demonstrating validation, cleaning, and transformation of input data.
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

```python
@zmag.gql
class Graphql:
    ...

    class Mutation:
        async def create(self, form: MyForm | None):
            if form and form.input.is_valid:
                print(form.input)
                print(form.input.dict(True))
                print(form.input.clean())
            return zmag.mutation()
```
