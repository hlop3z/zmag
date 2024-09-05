# -*- coding: utf-8 -*-
"""
Events
"""

import logging

# from zmag import settings

# print("DEBUG", settings.DEBUG)
# print("MODE", settings.MODE)


async def on_startup(context):
    """On Startup Event"""

    logging.info("demo.events: Server Startup")
    """
    logging.info(context)

    file = open("example.txt", "w")
    context.file = file
    logging.info("File is open.")
    """


async def on_shutdown(context):
    """On Shutdown Event"""

    logging.info("demo.events: Server Shutdown")
    """
    logging.info(context)

    if not context.file.closed:
        logging.info("File is open.")

    context.file.close()

    # Check if the file is closed after calling close()
    if context.file.closed:
        logging.info("File is closed.")
    else:
        logging.info("File is still open.")
    """
