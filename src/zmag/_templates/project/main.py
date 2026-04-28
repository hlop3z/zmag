from zmag.app import App

server = App()


@server.api.get("/")
async def hello():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    server.cli()
