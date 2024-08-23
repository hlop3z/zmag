# -*- coding: utf-8 -*-
"""
Components Network
"""

import functools
import inspect
import typing

from ...tools.timer import time_in_seconds
from .base import components


def pub(
    obj: typing.Any = None,
    *,
    channel: str | None = None,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
) -> typing.Any:
    """
    ZMQ `publisher` Creator.

    This function publishes `Data` to the `frontend`.

    Returns:
        (zmag.Data | None): Return `zmag.Data` if updates, `None` otherwise.

    Examples:
    ::

        @zmag.pub # or zmag.pub(seconds=5)
        async def topic(): # `topic` is the channel
            response = zmag.Data()
            response.body = {"message": "hello world"}
            return response

        @zmag.pub(seconds=5)
        async def generic(): # Custom `channel`
            response = zmag.Data()
            response.meta["channel"] = "custom"
            ...

        @zmag.pub
        async def graphql(context): # GraphQL
            gql_query = "query { books { id title } }"
            results = await context.schema.execute(gql_query)
            ...

    """
    if obj is None:
        return functools.partial(
            pub,
            channel=channel,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
        )
    # Real Wrapper
    the_channel = channel if isinstance(channel, str) else obj.__name__
    the_time = time_in_seconds(seconds=seconds, minutes=minutes, hours=hours, days=days)
    # Get Args
    signature = inspect.signature(obj)
    parameters = signature.parameters.keys()
    # Component
    config = {
        "channel": the_channel,
        "time": the_time,
        "context": "context" in parameters,
    }
    components.register("pub", obj, config)
    return obj


def push(
    obj: typing.Any = None,
    *,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
) -> typing.Any:
    """
    ZMQ `pusher` Creator.

    This function pushes `Data` to the `frontend`.


    Returns:
        (zmag.Data | None): Return `zmag.Data` if workload, `None` otherwise.

    Examples:
    ::

        @zmag.push # or zmag.push(seconds=5)
        async def push_method(): #
            response = zmag.Data()
            response.body = {"message": "hello world"}
            return response

        @zmag.push
        async def push_graphql(context): # GraphQL
            gql_query = "query { books { id title } }"
            results = await context.schema.execute(gql_query)
            ...
    """
    if obj is None:
        return functools.partial(
            push,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
        )
    # Real Wrapper
    the_time = time_in_seconds(seconds=seconds, minutes=minutes, hours=hours, days=days)
    # Get Args
    signature = inspect.signature(obj)
    parameters = signature.parameters.keys()
    # Component
    config = {
        "time": the_time,
        "context": "context" in parameters,
    }
    components.register("push", obj, config)
    return obj
