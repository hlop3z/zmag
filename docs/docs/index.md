# Welcome to **Zmag**

Zmag, is built with **Pyzmq (ZeroMQ)** and **Strawberry** this project is the sibling of [Fastberry](https://hlop3z.github.io/fastberry/)

The **`Command-Line-Interface` (CLI)** is built with **Click**.

<div id="terminal-index" data-termynal></div>

---

## **Description**

A tool for building **`GraphQL — API(s)`** with **`Python`**.

!!! info "You can create . . ."

    1. **`GraphQL`** — **`Query`**(s) and **`Mutation`**(s).
    3. **`Commands`** — To create automated processes and more . . .

---

## **Built** With

| Module                                                                                | Is Used To...                                                         |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| <a href="https://pyzmq.readthedocs.io" target="_blank">**Pyzmq**</a>                  | **API**'s core **Universal Messaging** **`Library`**.                 |
| <a href="https://strawberry.rocks/" target="_blank">**Strawberry**</a>                | **GraphQL** **`Library`**                                             |
| <a href="https://github.com/pallets/click/" target="_blank">**Click**</a>             | **Manage** the server, development process and custom **`Commands`**. |
| <a href="https://pypi.org/project/spoc/" target="_blank">**SPOC**</a>                 | **FrameWork** tool for building this **`Framework`**.                 |
| <a href="https://pypi.org/project/dbcontroller/" target="_blank">**DBController**</a> | **Database** Controller for **`SQL`** and **`Mongo`**.                |
| <a href="https://www.starlette.io/" target="_blank">**Starlette**</a>                 | **Run** the server in **`Debug`** mode.                               |

---

## Install **Zmag** (Demo)

```sh
python -m pip install "zmag[testing]"
```

## Install Zmag **Mongo**

```sh
python -m pip install "zmag[mongo]"
```

## Install Zmag **SQL**

```sh
python -m pip install "zmag[sql]" "databases[sqlite]"
```

!!! info "SQL Options"

    | Database   | Extra Installation(s)         |
    | ---------- | ----------------------------- |
    | PostgreSQL | **`"databases[postgresql]"`** |
    | MySQL      | **`"databases[mysql]"`**      |
    | Sqlite     | **`"databases[sqlite]"`**     |

---

## **Core** Layout

```text
root/                           --> <Directory> - Project's Root.
|
|-- apps/                       --> <Directory> - Project's Apps.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |-- development.toml   --> <File> - Development    | Settings.
|    |   |-- production.toml    --> <File> - Production     | Settings.
|    |   `-- staging.toml       --> <File> - Staging        | Settings.
|    |
|    |-- docs.md                --> <File> - API's Documentation in HERE.
|    |-- settings.py            --> <File> - API (Pythonic) | Settings.
|    `-- spoc.toml              --> <File> - API (TOML)     | Settings.
|
|-- pyproject.toml              --> <File> - Project (TOML) | Settings.
|
`-- etc...
```

---

## Inspired By **Django**

There are several things from Django that inspire this tool.

Some of the commands and the installation of **modules** (aka: **INSTALLED_APPS**) inside a Django project.

### **Zmag** comes with a few key **commands**:

| Command                     | Is Used To...                                             |
| --------------------------- | --------------------------------------------------------- |
| **`startproject`**          | Create a new **Zmag** project.                            |
| **`./manage.py run`**       | Run **FastApi Server**.                                   |
| **`./manage.py start-app`** | Create a **Zmag App** inside your "**`apps`**" directory. |
| **`./manage.py --help`**    | For **more information**.                                 |

!!! warning "startproject"

    Careful with the command `startproject`. Only **use it once** and make sure you are in a **new folder**.
    It will write files and folders.
