# -*- coding: utf-8 -*-
"""
Pushers
"""

import zmag

QUERY_STRING = """query MyQuery { demoBookList { id title } }"""


@zmag.push(seconds=1)
async def task_one(context):
    """Task 1"""
    results = await context.schema.execute(QUERY_STRING)
    response = zmag.Data()
    response.body = results.data
    return response


@zmag.push(seconds=5)
async def task_two():
    """Task 2"""
    response = zmag.Data()
    response.body = {"message": "from task two"}
    return response
