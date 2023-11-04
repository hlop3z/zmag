## `settings.py`

```python
# -*- coding: utf-8 -*-
"""
    { Settings }
"""

import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1] # (1)

# Installed APPS
INSTALLED_APPS = ["app_one", "app_two"] # (2)
```

1. The project's root directory
2. Zmag Apps currently in use.

## `spoc.toml`

```python
[spoc]
mode = "custom"
custom_mode = "development"

# GraphQL
[spoc.graphql]
max_depth = 4
max_limit = 100

# Database
[spoc.database]
engine = "sql"                  # options: mongo, sql
config = "sqlite:///example.db" # mongodb://localhost:59567/example_db

# Modes
[spoc.apps]
development = []
staging = []
production = []

```

## TOML Settings

| Key               | Description                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| **`custom_mode`** | Options: `development`, `production`, `staging`                                 |
| **`max_depth`**   | Object's max depth levels of nesting allowed in a GraphQL query.                |
| **`max_limit`**   | Max number of rows to retrieve per request from the Database                    |
| **`engine`**      | Options: `sql` or `mongo`                                                       |
| **`config`**      | Database's **connection_string**.                                               |
| **`spoc.apps`**   | `INSTALLED_APPS` inside the spoc's file and based on the selected `custom_mode` |

## Config Examples

!!! Info "For More Details Go To..."

    - [SQL Engine](https://pypi.org/project/databases/)
    - [Mongo Engine](https://pypi.org/project/motor/)

| Key      | Description                                                                        |
| -------- | ---------------------------------------------------------------------------------- |
| Mongo    | `mongodb://localhost:59567/your_database_name`                                     |
| SQLite   | `sqlite:///your_database_name.db`                                                  |
| Postgres | `postgresql://your_username:your_password@your_postgresql_host/your_database_name` |
| MySQL    | `mysql://your_username:your_password@your_mysql_host/your_database_name`           |
