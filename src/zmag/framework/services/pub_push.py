# -*- coding: utf-8 -*-
"""
ZMQ `Publisher` and `Pusher`
"""

import asyncio
from functools import partial


async def task_runner(server, node, interval, method, channel=None):
    """
    Task Runner that can either `publish` to a channel or `push` a message.
    """
    while server.active:
        message = await method()
        if message:
            if channel is not None:
                # PUB:
                # If a channel is provided, use `publish`
                the_channel = message.meta.get("channel", channel)
                await node.publish(the_channel, message)
            else:
                # PUSH:
                # If no channel is provided, use `push`
                await node.push(message)
        if interval > 0:
            await asyncio.sleep(interval)


async def start_pub_push(runner_type: str, server, app, node):
    """
    Start Task Runners for either pushers or publishers.
    """
    tasks = []
    context = app.context
    if runner_type == "pub":
        for method in app.publishers.values():
            with_ctx = method.info.config.get("context", False)
            tasks.append(
                task_runner(
                    server,
                    node,
                    method.info.config.get("time", 0),
                    partial(method.object, context) if with_ctx else method.object,
                    method.info.config.get("channel", ""),
                )
            )
    elif runner_type == "push":
        for method in app.publishers.values():
            with_ctx = method.info.config.get("context", False)
            tasks.append(
                task_runner(
                    server,
                    node,
                    method.info.config.get("time", 0),
                    partial(method.object, context) if with_ctx else method.object,
                )
            )

    await asyncio.gather(*tasks)


start_pusher = partial(start_pub_push, "push")
start_publisher = partial(start_pub_push, "pub")
