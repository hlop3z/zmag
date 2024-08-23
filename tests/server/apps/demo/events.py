# from zmag import settings

# print("DEBUG", settings.DEBUG)
# print("MODE", settings.MODE)


def on_startup(context):
    print("Server Startup")
    print(context)


def on_shutdown(context):
    print("Server Shutdown")
    print(context)
