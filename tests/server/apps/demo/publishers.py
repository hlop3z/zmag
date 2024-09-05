# -*- coding: utf-8 -*-
"""
Publishers
"""

import zmag

QUERY_STRING = """query { demoBookList { id title } }"""


@zmag.pub(seconds=1)
async def content(context):
    """Content"""
    results = await context.schema.execute(QUERY_STRING)
    response = zmag.Data()
    response.meta["channel"] = "custom"
    response.body = results.data
    return response


@zmag.pub(seconds=5, channel="custom_name")
async def topic():
    """Topic"""
    response = zmag.Data()
    response.body = {"message": "from my topic"}
    return response


@zmag.pub(seconds=1)
async def generic_demo():
    """Generic"""
    response = zmag.Data()
    response.body = {"message": "generic demo"}
    return response
