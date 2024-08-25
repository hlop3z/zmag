The code **must** be placed in a **file** named **`commands.py`** or in a **folder** named **`commands`** within the **Application directory**.

!!! note

    The **`zmag.cli`** especial wrapper for (aka: **`click.group`**) **must** be named **`cli`**.

## Examples

=== ":material-file: File"

    ```python title="commands.py"
    import zmag
    import click

    # Init Group
    @zmag.cli
    def cli():
        """Click (CLI) Group"""

    # Create <Commands> here.
    @cli.command()
    def hello_world():
        """Demo CLI Function"""

        click.echo("Hello World")
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    import zmag

    # Import <Commands> Here
    from .hello_world import hello_world

    # Init Group
    @zmag.cli
    def cli():
        """Click (CLI) Group"""

    # Register <Commands> Here
    cli.add_command(hello_world)
    ```

    ```python title="hello_world.py"
    import click


    # Create <Commands> here.
    @click.command()
    def hello_world():
        """Demo CLI Function"""

        print("Hello World")

    ```
