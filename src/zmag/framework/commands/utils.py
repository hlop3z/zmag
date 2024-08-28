# -*- coding: utf-8 -*-
"""
Core Commands Tools
"""


def get_imports():
    """Get Local Imports"""
    from ..framework import Framework  # pylint: disable=cyclic-import
    from ..services.runner import Server  # pylint: disable=cyclic-import

    return Framework, Server


def shell_banner(conf):
    """Shell Text Banner"""
    banner = ""
    hostname = "localhost" if conf.host == "0.0.0.0" else conf.host
    divider = "#" * 80 + "\n"

    # Text Options
    text_debug = "Enabled" if conf.debug else "Disabled"
    text_host = f"http://{hostname}:{conf.port}"
    text_device = conf.device.upper()
    text_workers = "Thread" if conf.thread else "Process"
    text_proxy = "Yes" if conf.proxy else "No"
    text_attach = "Yes" if conf.attach else "No"
    text_auth = "Yes" if conf.authentication else "No"

    if conf.debug:
        # Debug
        banner += divider
        banner += "[Hot-Reload] . . . (Press <CTRL + C> to quit)\n"
        banner += divider
        banner += f"* Debug Mode        : {text_debug}\n"
        banner += f"* Debug Server      : {text_host}\n"
    else:
        # Production
        banner += divider
        banner += "Starting ZMAG. . . (Press <CTRL + C> to quit)\n"

    # Shared
    banner += divider
    banner += f"* ZMQ Backend       : {conf.server}\n"
    if conf.attach or conf.proxy:
        banner += f"* ZMQ Frontend      : {conf.client}\n"
    banner += divider
    banner += f"* Device Type       : {text_device}\n"
    banner += f"* Start Proxy Device: {text_proxy}\n"
    banner += divider
    # Workers
    if conf.workers > 0:
        banner += f"* Authentication    : {text_auth}\n"
        banner += f"* Number of Workers : {conf.workers}\n"
        banner += f"* Worker Type       : {text_workers}\n"
        banner += f"* Connect to Proxy  : {text_attach}\n"
        banner += divider
    return banner
