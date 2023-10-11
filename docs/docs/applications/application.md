# Application (C.R.U.D **Default** Setup)

!!! info

    The **CRUD** application is created when you run the **`start-app`** command.

## **CRUD**

In this setup, all methods inside the **`Query`** and **`Mutation`** classes are automatically marked as static methods using **`@staticmethod`**. This means that when these functions are loaded after the server starts running, you won't need to use self within your functions.

### Command

```sh
./manage.py start-app my_app
```

### PyLint (**disable**)

!!! warning

    **E0213**: Method should have "**`self`**" as first argument (**no-self-argument**)

    Disable the **no-self-argument**.

### **Five Operations** to get you started.

> The demo-app comes with **`5`** core **`operations`**. (**Create, Update, Delete, Search** & **Detail**)

=== "GraphQL"

    | :material-pencil: Mutation     | :material-read: Query        |
    | ------------ | ------------ |
    | **`Create`** | **`Search`** |
    | **`Update`** | **`Detail`** |
    | **`Delete`** |              |

=== "CRUD"

    | Method       | CRUD        | GraphQL     | Description                                         |
    | ------------ | ----------- | ----------- | --------------------------------------------------- |
    | **`Create`** | Create      | `Mutation`  | :material-pencil:    Create resource                |
    | **`Update`** | Update      | `Mutation`  | :material-pencil:    Update resource                |
    | **`Delete`** | Delete      | `Mutation`  | :material-close:     Delete resource                |
    | **`Search`** | Read        | `Query`     | :material-read:      Fetch **Multiple** resources   |
    | **`Detail`** | Read        | `Query`     | :material-read:      Fetch **Single** resource      |

### Classes

- **`Query`**: GraphQL "**Query**" functions.
- **`Mutation`**: GraphQL "**Mutation**" functions.
- **`Meta`**: **Configurations** for the current GraphQL functions.

### **Meta** Variables (**optional**)

- **`app`** (**bool**) : Prepend the **application**'s name to the operation's name.
- **`model`** (**str**): Prepend **model**'s name to the operation's name.

```text
root/
|
|--  apps/
|    `--  MY_APP/
|         `-- graphql/            --> <Directory> - Your GraphQL in HERE!
|             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
|             |-- demo.py         --> <File> - Demo File.
|             `-- etc...
|
`-- etc...
```

## Demo **Files**

=== "demo.py"

    ```python
    # -*- coding: utf-8 -*-
    """
        API - GraphQL
    """

    # Zmag
    import zmag


    # Create your API (GraphQL) here.
    @zmag.gql
    class Demo:
        """Demo Api"""

        class Meta:
            """GQL-Class Metadata"""

            app = False
            model = None

        class Query:
            """Query"""

            async def search(info) -> str:
                """Read the Docs"""
                print(info)
                return "Search"

            async def detail(info) -> str:
                """Read the Docs"""
                print(info)
                return "Detail"

        class Mutation:
            """Mutation"""

            async def create(info) -> str:
                """Read the Docs"""
                print(info)
                return "Create"

            async def update(info) -> str:
                """Read the Docs"""
                print(info)
                return "Update"

            async def delete(info) -> str:
                """Read the Docs"""
                print(info)
                return "Delete"
    ```

=== "\_\_init\_\_.py"

    ```python
    # -*- coding: utf-8 -*-
    """
        GraphQL Operations
    """

    from .demo import Demo
    ```
