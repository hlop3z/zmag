# -*- coding: utf-8 -*-
"""
Generate CURVE Certificate Files
"""

from ...external import click
from ...network.keypair import keypair


@click.command()
def gen_keys() -> None:
    """Generate `CURVE` **Public** and **Private** Keys"""

    x_public, x_secret = keypair()

    public_text = f"""# PublicKey :  {x_public.decode("utf-8")}   #"""
    secret_text = f"""# SecretKey :  {x_secret.decode("utf-8")}   #"""

    max_length = max(len(public_text), len(secret_text))
    divider = "#" * max_length

    message = [
        divider,
        public_text,
        divider,
        secret_text,
        divider,
    ]

    click.echo("")
    click.echo("\n".join(message))
