## **Core** Layout

```text
folder/
|
|-- client.py                   --> <File> - Client Demo
|
|--  fragments/                 --> <Directory> - Fragments.
|    |-- author.graphql         --> <File> - GraphQL Fragment.
|    `-- etc...
|
`-- etc...
```

## Declaring Fragments

```graphql title="author.graphql"
# Used in: (filter, create_many, update_many)
fragment List on Author {
  id
  fullName
}

# Used in: (create, update, detail)
fragment Item on Author {
  id
  firstName
  lastName
  fullName
}
```

## Methods

| Name              | Fragment   | Description                   |
| ----------------- | ---------- | ----------------------------- |
| **`create`**      | **`Item`** | Create a single row           |
| **`update`**      | **`Item`** | Update a single row           |
| **`detail`**      | **`Item`** | Read a single row             |
| **`filter`**      | **`List`** | Read multiple row             |
| **`create_many`** | **`List`** | Create multiple rows          |
| **`update_many`** | **`List`** | Update multiple rows          |
| **`delete`**      | None       | Delete multiple/single row(s) |
| **`info`**        | None       | API's INFO                    |

## Starting a Client

```python title="client.py"
from pathlib import Path
from zmag import Client

CURRENT_PATH = Path(__file__).parent
FRAGMENTS_PATH = CURRENT_PATH / "fragments"

client = Client(
    host="tcp://127.0.0.1:5555",
    base_dir=FRAGMENTS_PATH,
    fragments={"Author": "author.graphql"},
)
```

## Demo Setup

```python
MODEL_NAME = "Author"
CONTEXT = {
    "user_id": 123,
}
```

## Create

```python
form_create = {
    "firstName": "John",  # John Michael Jane
    "lastName": "Doe",  # Doe Crichton Smith
}
response = client.create(MODEL_NAME, form=form_create, context=CONTEXT)
print(response)
```

## Update

```python
form_update = {
    "id": "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
    # "firstName": "Jane",
    "lastName": "Crichton",
}
response = client.update(MODEL_NAME, form=form_update, context=CONTEXT)
print(response)
```

## Detail

```python
item_id = "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ=="
response = client.detail(MODEL_NAME, id=item_id, context=CONTEXT)
print(response)
```

## Filter

```python
response = client.filter(MODEL_NAME, context=CONTEXT)
print(response)
```

## Create Many

```python
form_create_many = [
    {
        "firstName": "Michael",
        "lastName": "Crichton",
    },
    {
        "firstName": "Jane",  # Michael Jane
        "lastName": "Smith",  # Crichton Smith
    },
]
response = client.create_many(MODEL_NAME, forms=form_create_many, context=CONTEXT)
print(response)

```

## Update Many

```python
item_ids = [
    "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
    "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
]
form_update_many = {
    # "firstName": "Jane",
    "lastName": "Doe",
}
response = client.update_many(
    MODEL_NAME, ids=item_ids, form=form_update_many, context=CONTEXT
)
print(response)
```

## Delete

```python
item_ids = [
    "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
    "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
    "Mzo6NGQ0MDk4MzIxNjU0YTQ1Nw==",
]
response = client.delete(MODEL_NAME, ids=item_ids, context=CONTEXT)
print(response)
```

## Info

```python
response = client.info(context=CONTEXT)
print(response)
```
