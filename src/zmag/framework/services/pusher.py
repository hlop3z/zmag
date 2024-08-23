# -*- coding: utf-8 -*-
"""
ZMQ Pusher
"""

from types import SimpleNamespace
import asyncio
from functools import partial


async def start_pusher(server, app, node):
    """Start Pusher"""

    tasks = []
    for method in app.pushers.values():
        with_ctx = method.info.config.get("context", False)
        context = SimpleNamespace(
            schema=app.schema,
        )
        tasks.append(
            task_runner(
                server,
                node,
                method.info.config.get("time", 0),
                partial(method.object, context) if with_ctx else method.object,
            )
        )

    await asyncio.gather(*tasks)


async def task_runner(server, node, interval, method):
    """Task Runner"""
    while server.active:
        message = await method()
        if message:
            await node.push(message)
        if interval > 0:
            await asyncio.sleep(interval)
