import zmag

QUERY_STRING = """query { demoBookList { id title } }"""


@zmag.pub(seconds=1)
async def content(context):
    results = await context.schema.execute(QUERY_STRING)
    response = zmag.Data()
    response.meta["channel"] = "custom"
    response.body = results.data
    return response


@zmag.pub(seconds=5)
async def topic():
    response = zmag.Data()
    response.body = {"message": "hello world"}
    return response


@zmag.pub(seconds=1)
async def generic():
    response = zmag.Data()
    response.body = {"message": "generic demo"}
    return response
