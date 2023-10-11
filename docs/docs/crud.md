# GraphQL **CRUD** Operations for **Models**

This documentation offers a comprehensive guide to working with GraphQL operations in the context of models.

**`Operations`**: Discover a full suite of GraphQL operations encompassing Create, Read, Update, and Delete (**CRUD**) for models. Understand how to leverage GraphQL to efficiently handle model data, regardless of its complexity.

**`Forms`**: Learn how to define form classes tailored for GraphQL operations. You'll gain a solid understanding of creating and updating model instances using GraphQL and how to structure these forms effectively.

**`Manager`**: Explore the controller responsible for managing model-related database operations. This section delves into methods for searching, retrieving details, creating, updating, and deleting model records. It also addresses key considerations like permissions and query execution.

By the end of this documentation, you'll be well-equipped to harness the power of GraphQL for your model-driven applications. Whether you're dealing with Books, Users, or any other data entities, the principles covered here will be applicable and adaptable to your specific needs.

## Operations (CRUD)

```python title="graphql.py"
# -*- coding: utf-8 -*-
"""
    { CRUD } GraphQL(s)
"""

# Zmag
import zmag

# Type(s) Tools
from . import forms, manager

Books = zmag.crud(
    manager=manager.Book,
    form=forms.Book,
    clear_ignore=["author"],
    docs={},
)
```

## Forms

```python title="forms.py"
# -*- coding: utf-8 -*-
"""
    { Form } for the GraphQL's Operations
"""

# Zmag
import zmag

# Create your <forms> here.
@zmag.forms
class Book:
    class Create:
        """(Form) Read The Docs"""

        title = zmag.value(
            str,
            default=None,
            required=True,
        )

        author = zmag.value(
            str,
            default=None,
            required=True,
            rules=[],
        )

    class Update:
        """(Form) Read The Docs"""

        title = zmag.value(
            str,
            default=None,
        )

        author = zmag.value(
            str,
            default=None,
        )

```

## Manager

```python title="manager.py"
# -*- coding: utf-8 -*-
"""
    { Controller } for the Database(s)
"""

# Zmag
import zmag

from . import types

# Create your <managers> here.
@zmg.manager
class Book(zmg.BaseManager):
    """Book Manager"""

    model = types.Book

    @classmethod
    async def search(
        cls,
        context,
        pagination=None,
        query=None,
    ):
        print(context)

        # { PERMISSIONS }
        user_id = 2
        query = cls.filter_query_by_user_id(query, user_id)

        # { QUERY } Finally Run
        return await cls.objects.find(
            query,
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 10),
            sort_by=pagination.get("sort_by", "-id"),
        )

    @classmethod
    async def detail(cls, context, id=None, query=None):
        print(context)

        # { PERMISSIONS }
        user_id = 1
        active_query = cls.filter_query_by_user_id(query, user_id)
        print(active_query)

        # { QUERY } Finally Run
        return await cls.objects.find_one(active_query)

    @classmethod
    async def create(cls, context, form=None):
        print(context)

        # raise ValueError("author_name @ Author already registered")
        # raise PermissionError

        # { QUERY } Finally Run
        return await cls.objects.create(form)

    @classmethod
    async def update(cls, context, selected=None, form=None):
        print(context)

        # { PERMISSIONS }
        user_id = 1
        selected = await cls.get_ids_by_user_id(selected, user_id)

        # { QUERY } Finally Run
        print(selected, form)

        return await cls.objects.update(selected, form)

    @classmethod
    async def delete(cls, context, selected=None):
        print(context)

        # { PERMISSIONS }
        user_id = 1
        selected = await cls.get_ids_by_user_id(selected, user_id)

        # { QUERY } Finally Run
        return await cls.objects.delete(selected)
```

## Error Handling (**Manager**)

### Value

When raising an error, include a specific "**field/key**" and an associated "**error text**" as arguments to the error constructor.

For example: **`input_field @ My Error Message`**

```python title="manager.py"
raise ValueError("author_name @ Author already registered")
```

### Permission

```python title="manager.py"
raise PermissionError
```
