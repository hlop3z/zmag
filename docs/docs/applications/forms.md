> Your code **needs** to be in a **file** named **`forms.py`** or **folder** named **`forms`** inside your **Application**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- forms.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- forms/              --> <Directory> - Your Forms in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

!!! abstract "Tools"

    Zmag `input-values` can only have a **Single Typing**. You'll mainly use **3 tools** to create the **`forms`**.

    1. **`zmag.input(str)`**
    2. **`zmag.value`**
    3. **`zmag.filters(regex = list(tuple), rules = list(function))`**

## **Value** References

| Name           | API Reference                                                                        |
| -------------- | ------------------------------------------------------------------------------------ |
| **`default`**  | The **default** value                                                                |
| **`required`** | **Default: `False`**. Does the field **requires an input** value?                    |
| **`regex`**    | Regex (**validators**) **`key` = `Regex-Pattern`** and **`value` = `Error-Message`** |
| **`rules`**    | Custom (**validators**) returns **`None`** or **`Error-Message(s)`**                 |
| **`filters`**  | **Transform-Data** with **`Regex` & `Rules`**                                        |

## Python **Code**

!!! tip

    **Values** can only have a **Single Type**.

    **However**, you can wrap it around a **`list`** for example: **`list[int]`**

=== ":material-file: File"

    ```python title="forms.py"
    # -*- coding: utf-8 -*-
    """
        Forms - Complex Inputs
    """
    import zmag

    # Create Group "Form"
    form = zmag.input("form")

    # Create your <forms> here.

    @form  # (name="CustonInputName")
    class Search:
        """(Form) Read The Docs"""

        name = zmag.value(
            # Single Typing
            str,
            default=None,
            required=True,
        )
        count = zmag.value(
            int,
            default=999,
        )
        cash = zmag.value(
            float,
            default=44.4,
        )
        amount = zmag.value(
            zmag.decimal,
            default="55.5",
        )
        start_date = zmag.value(
            zmag.date,
            default="2022-11-10",
        )
        end_datetime = zmag.value(
            zmag.datetime,
            default="2022-11-10T16:35:56.216344",
        )
        timestamp = zmag.value(
            zmag.time,
            default="16:35:04.872130",
        )


    @form
    class User:
        """(Complex-Form) Read The Docs"""

        email = zmag.value(
            str,
            default="demo@helloworld.com",
            regex={
                r"[\w\.-]+@[\w\.-]+": "invalid email address"
            },
            rules=[
                (lambda v: v.startswith("demo") or "invalid input")
            ],
            filters=zmag.filters(
                regex=[
                    ("^hello", "hola"),
                    ("com", "api"),
                ],  # ("^hello"...) [Won't Work]: We used { regex } to check if it startswith "hello".
                rules=[
                    (lambda v: v.upper())
                ],
            ),
        )
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        Forms - Init
    """

    # Import your <cruds> here.
    from .demo import Search, User
    ```

    ``` python title="demo.py"
    # -*- coding: utf-8 -*-
    """
        API - Complex Inputs
    """

    # Zmag
    import zmag

    # Create Group "Form"
    form = zmag.input("form")

    # Create your API (GraphQL) here.

    @form  # (name="CustonInputName")
    class Search:
        """(Form) Read The Docs"""

        name = zmag.value(
            str,  # Single Typing
            default=None,
        )
        count = zmag.value(
            int,
            default=None,
        )
        cash = zmag.value(
            float,
            default=None,
        )
        amount = zmag.value(
            zmag.decimal,
            default=None,
        )
        start_date = zmag.value(
            zmag.date,
            default=None,
        )
        end_datetime = zmag.value(
            zmag.datetime,
            default=None,
        )
        timestamp = zmag.value(
            zmag.time,
            default=None,
            required=True,
        )

    @form
    class User:
        """(Complex-Form) Read The Docs"""

        email = zmag.value(
            str,
            default="demo@helloworld.com",
            regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
            rules=[(lambda v: v.startswith("demo") or "invalid input")],
            filters=zmag.filters(
                regex=[
                    ("^hello", "hola"),
                    ("com", "api"),
                ],  # ("^hello"...) [Doesn't Work]: We used { regex } to check if it startswith "hello".
                rules=[(lambda v: v.upper())],
            ),
        )
    ```
