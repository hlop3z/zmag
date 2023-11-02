"""
    Core { Commands }
"""
import click

# Import Commands Here
from .run_server import run
from .sql_alembic import ALEMBIC_CONFIG, db
from .graphql_schema import schema
from .start_app import start_app


@click.group()
def cli():
    "Click (CLI)"


# Register Commands
cli.add_command(run)
cli.add_command(schema)
cli.add_command(start_app)

if ALEMBIC_CONFIG:
    cli.add_command(db)
