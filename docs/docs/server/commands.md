# Commands

To set up commands in your ZMAG application, the code **must** be located in a **file** named **`commands.py`** or in a **folder** named **`commands`** within the **application directory**.

!!! note

    **`zmag.cli`** is a specialized wrapper for `click.group`.

The primary distinction between `click` and `zmag` commands is that `zmag` adds predefined configurations and can infer certain settings, such as `type`, `required`, and `default`, directly from function parameters. This makes the implementation more Pythonic and compatible with type hints.

---

## CLI Tools — [Reference](/{{ url("/api/cli") }})

- **`zmag.cli`** — Interface for creating `click.Group` commands.
- **`zmag.cli.argument`** — A wrapper around `click.argument`.
- **`zmag.cli.option`** — A wrapper around `click.option`.
- **`zmag.cli.range`** — A wrapper around `click.IntRange` and `click.FloatRange`.
- **`zmag.coro`** — Transform an `asynchronous` function into a `synchronous` function.

!!! tip

    Use these tools for creating CLI commands in your application.

---

## Examples

### Basic Command Example

```python title="commands.py"
import zmag

# Initialize CLI group
@zmag.cli.group
def cli():
    """Main CLI group."""

# Define commands here
@cli.command()
def hello_world():
    """Demo command that prints a message."""

    zmag.cli.echo("Hello World (Command)")
```

**Terminal Output:**

<!-- termynal -->

```
$ python main.py hello-world
Hello World (Command)
```

### Sub-Group Example

```python title="commands.py"
import zmag

# Initialize CLI group
@zmag.cli
def cli():
    """Main CLI group."""

# Initialize subgroup
@zmag.cli(group=True)
def database():
    """Database operations group."""

# Define commands within subgroup
@database.command()
def migrate():
    """Command to migrate the database."""

    zmag.cli.echo("Migrate (Database)")

# Attach subgroup to main CLI
cli.add_command(database)
```

**Terminal Output:**

<!-- termynal -->

```
$ python main.py database migrate
Migrate (Database)
```

### Coroutine Command Example

```python
@cli.command()
@zmag.coro # (1)
async def hello_world():
    """Demo async command."""
```

1. Transform `asynchronous` function into a `synchronous` function.

### Typing Example with `Arguments` and `Options`

```python
from typing import Literal
from datetime import datetime
from pathlib import Path

@cli.command()
@zmag.cli.argument("message", help="Custom help message.")
@zmag.cli.argument("count", help="Number of times to repeat the message.")
@zmag.cli.option("--folder", help="Path to a folder.")
@zmag.cli.option("--when", help="Timestamp for the operation.")
@zmag.cli.option("--logging", help="Logging level.")
@zmag.cli.option("--scale", type=zmag.cli.range(1, 5), help="Scale between 1 and 5.")
@zmag.cli.option("--scope", type=zmag.cli.range(1.0, 5.0), help="Scope between 1.0 and 5.0.")
def hello_world(
    message: str,  # Required (1)
    count: int | None,  # Optional (2)
    folder: Path | None = None,  # Path (3)
    when: datetime | None = None,  # Datetime (4)
    logging: Literal["level_one", "level_two"] | None = None,  # Choice (5)
    scale: int | None = None, # with click.IntRange
    scope: float | None = None, # with click.FloatRange
):
    """Demo command that demonstrates various options and arguments."""
```

1. **Required field** `(required=True)`.
2. **Optional field** `(required=False)`.
3. **Path type** uses `click.Path`.
4. **Datetime type** uses `click.DateTime`.
5. **Choice type** uses `click.Choice`.

!!! tip

    - For choices use `typing.Literal`.
    - To mark a field as optional use `<type> | None`.
