# Welcome to **Zmag**

Zmag, is built with **Pyzmq (ZeroMQ)** and **Ariadne (GraphQL)** this project is the sibling of [Fastberry](https://hlop3z.github.io/fastberry/)

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
| <a href="https://ariadnegraphql.org/" target="_blank">**Ariadne**</a>                 | **GraphQL** **`Library`**                                             |
| <a href="https://github.com/pallets/click/" target="_blank">**Click**</a>             | **Manage** the server, development process and custom **`Commands`**. |
| <a href="https://pypi.org/project/spoc/" target="_blank">**SPOC**</a>                 | **FrameWork** tool for building this **`Framework`**.                 |
| <a href="https://pypi.org/project/dbcontroller/" target="_blank">**DBController**</a> | **Database** Controller for **`SQL`** and **`Mongo`**.                |
| <a href="https://www.starlette.io/" target="_blank">**Starlette**</a>                 | **Run** the server in **`Debug`** mode.                               |

---

## Install **Zmag** (Development)

```sh
python -m pip install "zmag[debug]"
```

## Install **Zmag** (Client)

```sh
python -m pip install "zmag"
```

## Install Zmag **Mongo**

```sh
python -m pip install "zmag[mongo]"
```

## Install Zmag **SQLite**

```sh
python -m pip install "zmag[sqlite]"
```

## Install Zmag **PostgreSQL**

```sh
python -m pip install "zmag[sqlite]"
```

## Install Zmag **MySQL**

```sh
python -m pip install "zmag[mysql]"
```

---

## **Core** Layout

```text
root/                           --> <Directory> - Project's Root.
|
|-- apps/                       --> <Directory> - Project's Apps.
|
|--  config/                    --> <Directory> - Configurations.
|    |-- settings.py            --> <File> - API (Pythonic) | Settings.
|    `-- spoc.toml              --> <File> - API (TOML)     | Settings.
|
`-- etc...
```

---

### **Zmag** comes with a few key **commands**:

| Command                   | Is Used To...                                             |
| ------------------------- | --------------------------------------------------------- |
| **`startproject`**        | Create a new **Zmag** project.                            |
| **`./main.py run`**       | Run **Server**.                                           |
| **`./main.py start-app`** | Create a **Zmag App** inside your "**`apps`**" directory. |
| **`./main.py db`**        | **SQL** (only) Alembic **Migrations**.                    |
| **`./main.py --help`**    | For **more information**.                                 |

!!! warning "startproject"

    Careful with the command `startproject`. Only **use it once** and make sure you are in a **new folder**.
    It will write files and folders.
