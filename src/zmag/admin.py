"""Bootstrap CLI: ``zmag-init <project_name>`` scaffolds a new project.

This module intentionally avoids importing anything from the rest of ``zmag``
that depends on a project being present (``app``, ``migrations``, ``apps``).
It runs *before* a project exists, so its only deps are ``click`` + stdlib.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import click

_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_TEMPLATES_DIR = Path(__file__).parent / "_templates" / "project"


def _render(text: str, project_name: str) -> str:
    return text.replace("{{PROJECT_NAME}}", project_name)


def _copy_tree(src: Path, dst: Path, project_name: str) -> None:
    for entry in src.iterdir():
        target = dst / entry.name
        if entry.is_dir():
            target.mkdir(exist_ok=True)
            _copy_tree(entry, target, project_name)
            continue
        try:
            text = entry.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            target.write_bytes(entry.read_bytes())
            continue
        target.write_text(_render(text, project_name), encoding="utf-8")


@click.command(name="zmag-init")
@click.argument("project_name")
def main(project_name: str) -> None:
    """Scaffold a new zmag project at ./<PROJECT_NAME>/."""
    if not _NAME_RE.match(project_name):
        click.echo(
            click.style(
                f"Error: {project_name!r} is not a valid Python identifier.",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)

    if not _TEMPLATES_DIR.exists():
        click.echo(
            click.style(
                f"Error: project template missing at {_TEMPLATES_DIR}.", fg="red"
            ),
            err=True,
        )
        sys.exit(1)

    target = Path.cwd() / project_name
    if target.exists() and any(target.iterdir()):
        click.echo(
            click.style(f"Error: {target} already exists and is not empty.", fg="red"),
            err=True,
        )
        sys.exit(1)

    target.mkdir(exist_ok=True)
    _copy_tree(_TEMPLATES_DIR, target, project_name)

    click.echo(click.style(f"Created project at {target}", fg="green", bold=True))
    click.echo(click.style("Next steps:", bold=True))
    click.echo(f"  cd {project_name}")
    click.echo("  uv sync")
    click.echo("  uv run python main.py db init")
    click.echo("  uv run python main.py run --dev")


if __name__ == "__main__":
    main()
