Creating Schema Types

## Table Name (`kebab-case`)

The name of the Model, Type, or Table in your database, following kebab-case naming convention.

## Engine

Specifies the type of database to be used, either **SQL** or **Mongo**.

## Config

The `config` section contains various keys for configuring your database schema:

| Key                   | Type            | Description                                        |
| --------------------- | --------------- | -------------------------------------------------- |
| **`table_name`**      | str             | Statically declared table name in the database     |
| **`primary_key`**     | list[str]       | Fields indexed by the database as primary keys     |
| **`required`**        | list[str]       | Fields marked as `NOT NULL` in the database        |
| **`unique`**          | list[str]       | Fields that must be unique in the database         |
| **`unique_together`** | list[list[str]] | Fields that must be unique together in combination |
| **`ignore`**          | list[str]       | Fields computed and resolved by a function         |
| **`auto`**            | list[str]       | Fields that do not require user input              |

## Schema Scalar Fields

These are the available scalar fields in your schema with their Python data types and corresponding SQL field types:

| Key             | Python Type       | SQL Fields         |
| --------------- | ----------------- | ------------------ |
| **`$string`**   | str               | String(length=255) |
| **`$integer`**  | int               | Integer            |
| **`$float`**    | float             | Float              |
| **`$boolean`**  | bool              | Boolean            |
| **`$date`**     | datetime.date     | Date               |
| **`$time`**     | datetime.time     | Time               |
| **`$datetime`** | datetime.datetime | DateTime           |
| **`$decimal`**  | decimal.decimal   | String(length=255) |
| **`$text`**     | dbcontroller.text | Text               |
| **`$dict`**     | dbcontroller.json | JSON               |
| **`$list`**     | dbcontroller.json | JSON               |

### Note

All scalar fields start with a "**`$`**" symbol. When you create your own custom type, you can reference it without the "**`$`**" symbol or any other special character. For example:

```python
{
    "schema": {
        "book": "book",   # Single
        "books": ["book"], # Multiple
    }
}
```

## Schema Demo

```python
import zmag

@zmag.schema
class Schema:
    types = [
        {
            "name": "author",
            "engine": "sql",
            "config": {
                "ignore": ["full_name"],
            },
            "schema": {
                "first_name": "$string",
                "last_name": "$string",
                "full_name": "$string",
                "books": ["book"],
            },
        },
        {
            "name": "book",
            "engine": "sql",
            "config": {
                "auto": ["timestamp"],
            },
            "schema": {
                "title": "$string",
                "author": "author",
                "timestamp": "$datetime",
            },
        },
    ]
```
