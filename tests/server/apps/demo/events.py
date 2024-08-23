# from zmag import settings

# print("DEBUG", settings.DEBUG)
# print("MODE", settings.MODE)


def on_startup(app):
    print("Server Startup")
    print(app.info)


def on_shutdown(app):
    print("Server Shutdown")
    print(app.info)
