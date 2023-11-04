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
fragment List on Author {
  id
  fullName
}
fragment Item on Author {
  id
  firstName
  lastName
  fullName
}
```

## Starting Client

```python title="client.py"
from pathlib import Path

CURRENT_PATH = Path(__file__).parent
FRAGMENTS_PATH = CURRENT_PATH / "fragments"

client = Client(
    host="tcp://127.0.0.1:5555",
    base_dir=FRAGMENTS_PATH,
    fragments={"Author": "author.graphql"},
)
```

## Methods

| Name              | Description          |
| ----------------- | -------------------- |
| **`create`**      | Create a single row  |
| **`update`**      | Update a single row  |
| **`delete`**      | Delete a single row  |
| **`create_many`** | Create multiple rows |
| **`update_many`** | Update multiple rows |
| **`detail`**      | Read a single row    |
| **`filter`**      | Read a multiple row  |
| **`info`**        | API's INFO           |
