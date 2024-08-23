The code **must** be placed in a **file** named **`graphql.py`** or within a **folder** named **`graphql`** located in the **Application directory**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- graphql.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- graphql/            --> <Directory> - Your GraphQL in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

=== ":material-file: File"

    ``` python title="graphql.py"
    # -*- coding: utf-8 -*-
    """
        API - GraphQL
    """

    # ZMAG
    import zmag


    # Create your API (GraphQL) here.
    @zmag.gql
    class Demo:
        """Demo Api"""

        class Query:
            """Query"""

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
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        GraphQL - Init
    """

    # Import your <cruds> here.
    from .demo import Demo
    ```

    ``` python title="demo.py"
    # -*- coding: utf-8 -*-
    """
        API - GraphQL
    """

    # ZMAG
    import zmag


    # Create your API (GraphQL) here.
    @zmag.gql
    class Demo:
        """Demo Api"""

        class Query:
            """Query"""

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
    ```
