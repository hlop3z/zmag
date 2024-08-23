import zmag

QUERY_STRING = """query MyQuery { demoBookList { id title } }"""


@zmag.push(seconds=1)
async def task_one(context):
    results = await context.schema.execute(QUERY_STRING)
    response = zmag.Data()
    response.body = results.data
    return response


@zmag.push(seconds=5)
async def task_two():
    response = zmag.Data()
    response.body = {"message": "hello world"}
    return response
