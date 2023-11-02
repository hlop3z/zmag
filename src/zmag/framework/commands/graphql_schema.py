import click


@click.command()
def schema():
    """GraphQL Schema."""
    from .. import Framework

    # App
    app = Framework()

    click.secho(app.graphql_schema)
