# -*- coding: utf-8 -*-
"""
Generate `CURVE` **Public** and **Private** Keys"
"""

# ZMQ
import zmq


def keypair() -> tuple[bytes, bytes]:
    """
    Generate `CURVE` **Public** and **Private** Keys

    Example:

    `public_key, secret_key = zmag.keypair()`

    """

    return zmq.curve_keypair()  # pylint: disable=no-member
