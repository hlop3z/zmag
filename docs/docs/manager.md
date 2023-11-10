# Type Manager

This tool is designed for **GraphQL Type(s)** management and resolving. Type management encompasses structuring and managing relationships among GraphQL types, enabling the modeling of data hierarchies and connections with other types.

## Model/Type Definition

This function defines a model with a specified `kebab-case-name`.

## Arguments

- `name` (str): The name of the model.

**Model Example:**

```python
import zmag

Author = zmag.type("book-author")
```

## **`field`** decorator

You can resolve a field for the model using the `@<model_name>.field` decorator.

**Example:**

```python
@Author.field("full_name")
async def resolve_full_name(obj, info):
    return obj.get("first_name", "") + " " + obj.get("last_name", "")
```

## **`perms`** decorator

Options: **`('update', 'delete', 'detail', 'filter')`**

Specify permissions for the model using the `@<model_name>.perms` decorator.

**Example:**

```python
@Author.perms("update")
async def check_object_perms(obj, info):
    user_id = info.context.get("user_id")
    if obj.user_id != user_id:
        return None
    return obj
```

## **`form`** decorator

You can define forms for 'create' and 'update' operations using the `@<model_name>.form` decorator.

**Example:**

```python
@Author.form("update")
class Update:
    first_name = zmag.value(
        str,
        default=None,
        required=False,
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )
    last_name = zmag.value(
        str,
        required=True,
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )
```

## **`after`** decorator

Options: **`('create', 'update', 'delete', 'detail', 'filter')`**

Define actions to be performed after operations using the `@<model_name>.after` decorator.

**Example:**

```python
@Author.after("filter")
async def after_method(response, info):
    print("After everything is ready and done")
```

## **`filter`** decorator

Options: **`('computed', 'query')`**

Specify filter options for the model using the `@<model_name>.filter` decorator.

**Computed Example:**

```python
@Author.filter("computed")
async def dataset_computed_value(response, info):
    return {"computed_value": len(response.data)}
```

**Query Example:**

```python
@Author.filter("query")
async def preset_query(lookup, context=None):
    perms_query = lookup.query([
        ["last_name", "contains", "doe"],
        "or",
        ["last_name", "contains", "crichton"],
    ])
    perms_query &= lookup.query([
        ["_id", "eq", 1]
    ])
    return perms_query
```
