# Resources APIs

```python
("field", "perms", "util", "rule", "form", "after")
```

```python
Book = model("book")
```

## **`@<model>.field`**

## **`@<model>.perms`**

- **`update`**
- **`delete`**
- **`detail`**
- **`filter`**

## **`@<model>.after`**

- **`create`**
- **`update`**
- **`delete`**
- **`detail`**
- **`filter`**

## **`@<model>.filter`**

- **`query`**
- **`computed`**

```python
@Author.field("full_name")
@Author.perms("filter") # update, delete, detail, filter
@Author.after("create") # create, update, delete, detail, filter
@Author.filter("computed") # computed, query
```

```python
@Author.field("full_name")
async def resolve_full_name(obj, info):
    return obj.get("first_name", "") + " " + obj.get("last_name", "")

@Author.perms("update")
async def check_object_perms(obj, info):
    user_id = info.context.get("user_id")
    if obj.user_id != user_id:  # disable object from being updated
        return None
    return obj

@Author.after("filter")
async def check_object_perms(response, info):
    print("After everything is ready and done")

@Author.filter("computed")
async def dataset_computed_value(response, info):
    return {"computed_value": len(response.data)}

@Author.filter("query")
async def preset_query(lookup, context=None):
    perms_query = lookup.query([
        ["last_name", "contains", "doe"],
        "or",
        ["last_name", "contains", "crichton"],
    ])
    perms_query &= lookup.query([["_id", "eq", 1]])
    return perms_query
```
