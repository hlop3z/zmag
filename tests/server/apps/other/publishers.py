import zmag


@zmag.pub(seconds=1)
async def generic():
    response = zmag.Data()
    response.body = {"message": "generic other"}
    return response
