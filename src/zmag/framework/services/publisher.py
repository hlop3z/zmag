# -*- coding: utf-8 -*-
"""
ZMQ Publisher
"""

from types import SimpleNamespace
import asyncio
from functools import partial


async def start_publisher(server, app, node):
    """Start Publisher"""
    tasks = []
    for method in app.publishers.values():
        with_ctx = method.info.config.get("context", False)
        context = SimpleNamespace(
            schema=app.schema,
        )
        tasks.append(
            task_runner(
                server,
                node,
                method.info.config.get("time", 0),
                method.info.config.get("channel", ""),
                partial(method.object, context) if with_ctx else method.object,
            )
        )

    await asyncio.gather(*tasks)


async def task_runner(server, node, interval, channel, method):
    """Task Runner"""
    while server.active:
        message = await method()
        if message:
            the_channel = message.meta.get("channel", channel)
            await node.publish(the_channel, message)
        if interval > 0:
            await asyncio.sleep(interval)
