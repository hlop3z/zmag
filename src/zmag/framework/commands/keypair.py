# -*- coding: utf-8 -*-
"""
Generate CURVE Certificate Files
"""

import json as py_json

import click

from ...network.keypair import keypair


@click.command()
@click.option("-j", "--json", is_flag=True, help="JSON format")
def gen_keys(json) -> None:
    """Generate Public and Private Keys (CURVE)"""

    x_public, x_secret = keypair()
    public_key, secret_key = x_public.decode("utf-8"), x_secret.decode("utf-8")

    if json:
        json_message = {
            "public_key": public_key,
            "secret_key": secret_key,
        }
        click.echo(py_json.dumps(json_message, indent=4))
    else:
        list_message = [
            "[env.zmq]",
            f'''public_key = "{public_key}"''',
            f'''secret_key = "{secret_key}"''',
        ]
        click.echo("\n".join(list_message))
