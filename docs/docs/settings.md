Core **Settings** are in **`TOML`** format. Because **TOML** is easy to read for humans and computers.

!!! example "TOML"

    Since <a href="https://toml.io/en/" target="_blank">**`TOML`**</a>  is **`Python`**'s new best friend. Feels like a good fit for the core **settings** of the project.

---

## Settings **Workflow**

!!! info "Settings"

    1. Load **`pyproject.toml`**
    2. Load **`spoc.toml`**
    3. Load **`settings.py`**
    4. Load **`Environment Variables`**

```mermaid
flowchart TB;
    A[pyproject.toml] --> E{Project Settings};
    B[spoc.toml] --> E{Project Settings};
    C[settings.py] --> E;
    D[environment.toml] --> E;
```

---

## Settings **Locations**

```text
root/                           --> <Directory> - Project's Root.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |-- development.toml   --> <File> - Development Settings.
|    |   |-- production.toml    --> <File> - Production Settings.
|    |   `-- staging.toml       --> <File> - Staging Settings.
|    |
|    |-- settings.py            --> <File> - Pythonic Settings.
|    `-- spoc.toml              --> <File> - Spoc Settings.
|
|-- pyproject.toml              --> <File> - PyProject Settings.
`-- etc...
```

=== "PyProject"

    ## **pyproject** (TOML)

    ``` toml title="pyproject.toml"
    [project]
    name = "zmag" # (1)
    version = "0.1.4" # (2)
    description = "GraphQL Made Easy." # (3)

    # etc ... (4)
    ```

    1. **Name** — The **name** of the project.
    2. **Version** — The **version** of the project.
    3. **Description** — Short **description** of your project.
    4. **Other** — Extra **configurations** of your project.

    !!! info "PyProject"

        **`zmag.config["pyproject"]`** is where your **PyProject Variables** are loaded.

    ``` python title="example.py"
    import zmag

    print(zmag.config["pyproject"])
    ```

=== "Spoc"

    ## **SPOC** (TOML)

    ``` toml title="config/spoc.toml"
    [spoc] # (1)
    mode = "custom" # development, production, staging, custom
    custom_mode = "development" # (2)

    [spoc.api] # (3)
    max_depth = 4 # (4)
    items_per_page = 50 # (5)

    [spoc.apps] # (6)
    production = ["app_one", "app_two"] # (7)
    development = [] # (8)
    staging = [] # (9)

    [spoc.extras] # (10)
    extensions = ["zmag.extras.extensions"] # (11)
    permissions = ["zmag.extras.permissions"] # (12)
    ```

    1. **API** — **Core Settings**.
    2. **Custom** — Custom mode will load **`Apps`** from the pythonic **`settings.py`** plus the current **`mode`**.
    3. **API** — **Querying & More Configs**.
    4. **Depth** — Search depth in the GraphQL's **tree**.
    5. **Pagination** — Number of **rows per page**.
    6. **Installed** — **Apps**.
    7. **Production** — Production Ready Apps **(`Production`)**.
    8. **Development** — Development Only Apps **(`Production` + `Development`)**.
    9. **Staging** — Testing Only Apps **(`Production` + `Staging`)**.
    10. **Installed** — **Extension & Permissions**.
    11. **Extensions** — For adding behavior that is applied across your entire **(GraphQL)** application.
    12. **Permissions** — For adding **Permissions** to your **(GraphQL)** application.

    !!! info "SPOC"

        **`zmag.config["spoc"]`** is where your **SPOC Variables** are loaded.

    ``` python title="example.py"
    import zmag

    print(zmag.config["spoc"])
    ```

=== "Environment Variables"

    ## **Environment Variables** (TOML)

    ``` toml title="config/.env/development.toml"
    [env]
    DEBUG       = "yes"
    SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
    ```

    !!! info "Variables"

        **`zmag.config["env"]`** is where your **Environment Variables** are loaded.

    ``` python title="example.py"
    import zmag

    print(zmag.config["env"])
    ```

=== "Custom (settings.py)"

    ## **Custom** (Python)

    ``` python title="settings.py"
    # -*- coding: utf-8 -*-
    """
        { Settings }
    """
    import pathlib

    # Base Directory
    BASE_DIR = pathlib.Path(__file__).parents[1]

    # Installed Apps
    INSTALLED_APPS = ["good_app", "app_two"]

    # Database(s)
    DATABASES = {
        "sql"  : {"default": "sqlite:///example.db"},
        "mongo": {"default": "mongodb://localhost:27017/example"},
    }
    ```

    !!! info "PyProject"

        **`zmag.config["pyproject"]`** is where your **PyProject Variables** are loaded.

    ``` python title="example.py"
    import zmag

    print(zmag.config["pyproject"])
    ```

## **Breakdown** of the **Extensions and Permissions**

---

#### EXTENSIONS <a href="https://strawberry.rocks/docs/guides/custom-extensions" target="_blank" rel="noopener noreferrer">**(Strawberry)**</a>

> List of active **Extensions**.

You can create your own **`extension`** by using the **base module**.

The **`BaseExtension`** included is just a wrapper/rename for **Extension** from **Strawberry**

---

#### PERMISSIONS <a href="https://strawberry.rocks/docs/guides/permissions" target="_blank" rel="noopener noreferrer">**(Strawberry)**</a>

> List of active **Permissions**.

You can create your own **`permissions`** by using the **base module**.

The **`BasePermission`** included is just a wrapper for **BasePermission** from **Strawberry**
