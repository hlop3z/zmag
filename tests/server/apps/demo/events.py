# -*- coding: utf-8 -*-
"""
Events
"""

# from zmag import settings

# print("DEBUG", settings.DEBUG)
# print("MODE", settings.MODE)


def on_startup(context):
    """On Startup Event"""

    print("Server Startup")
    print(context)


def on_shutdown(context):
    """On Shutdown Event"""

    print("Server Shutdown")
    print(context)
