# Scalars

ZMAG provides wrappers for various scalars, including from Strawberry, to centralize and simplify imports. This reduces the need for multiple import statements in Python files, keeping the code cleaner and more streamlined.

!!! note "strawberry"

    To create custom scalars or learn more about how they work, visit the official documentation [here](https://strawberry.rocks/docs/types/scalars).

| GraphQL    | Python          |
| ---------- | --------------- |
| `String`   | `str`           |
| `Int`      | `int`           |
| `Float`    | `float`         |
| `Boolean`  | `bool`          |
| `ID`       | `zmag.id`       |
| `Decimal`  | `zmag.decimal`  |
| `Date`     | `zmag.date`     |
| `Time`     | `zmag.time`     |
| `DateTime` | `zmag.datetime` |
| `UUID`     | `zmag.uuid`     |
| `JSON`     | `zmag.json`     |

## Example

```python
from dataclasses import dataclass
import zmag

@dataclass
class Product(zmag.Type):
    id: zmag.id
    serial: zmag.uuid
    name: str
    stock: int
    weight: float
    is_available: bool
    available_from: zmag.date
    same_day_shipping_before: zmag.time
    created_at: zmag.datetime
    price: zmag.decimal
    metadata: zmag.json
```

<style>
.md-typeset__table {
    min-width: 200px !important;
}
</style>
