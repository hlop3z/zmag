"""
Built-in Forms for GraphQL.
"""

import orjson
import strawberry

from ..external import SPOC
from ..framework.components import Input, graphql_input
from ..framework.components.forms import form_field, value_cleaner

Form = graphql_input()

ITEMS_PER_PAGE = SPOC.settings.SPOC.get("graphql", {}).get("items_per_page", 100)

ITEM_DOC = """
**Selector** for database **Record(s)** by **ID(s)**.
"""

PAGINATION_DOC = """
---

### **All**: 

`(all: true)`

- **Description**: Returns **all items** in the **database**. This setting is primarily intended for **administrative purposes** and should be used with caution.

---

### **jsonQuery**: 

`(jsonQuery: "[{\\"key\\":1}]")`

- **Description**: Allows filtering through JSON queries. This is particularly useful for special cases where more complex filtering criteria are required.

---

### **Note**: 

- Use these settings wisely, especially the `all` setting, as it can impact performance by loading all records from the database.
"""


def load_json(value):
    """Load JSON"""
    if value:
        output = None
        try:
            output = orjson.loads(value)  # pylint: disable=E
        finally:
            pass
        return output
    return value


@Form(description=ITEM_DOC)
class GenericSelector(Input):
    """
    A utility for `selecting` database record(s).

    Example:

    ```python
    class Query:
        async def detail(self, record: zmag.Selector):
            ...
    ```
    """

    class Next:
        """Run After User-Input"""

        id: int = 0
        ids: list = []

        def run(self):
            """Run"""

            self.is_many = False
            if self.id is None and self.ids is not None:
                self.is_many = True

    id: strawberry.ID = form_field(default=None)
    ids: list[strawberry.ID] = form_field(default=None)


@Form(description=PAGINATION_DOC)
class GenericPagination(Input):
    """
    An input for managing pagination, for efficient `navigation` and retrieval of database records.

    Example:

    ```python
    class Query:
        async def search(self, pagination: zmag.Pagination):
            ...
    ```
    """

    class Next:
        """Run After User-Input"""

        page = 0
        limit = 10

        def run(self):
            """Run"""

            self.page = max(1, self.page)
            self.limit = min(ITEMS_PER_PAGE, self.limit)

    limit: int = form_field(default=ITEMS_PER_PAGE)
    page: int = form_field(default=1)
    sort_by: str = form_field(default="-id")
    all: bool = form_field(default=False)
    json_query: str = form_field(
        default=None,
        clean=value_cleaner(
            rules=[load_json],
        ),
    )
