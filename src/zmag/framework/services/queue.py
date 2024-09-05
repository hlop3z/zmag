# -*- coding: utf-8 -*-
"""
{ Queue }
"""

from types import SimpleNamespace


async def start_queue(server, app, node):
    """Start Queue"""
    while server.active:
        # ZMQ Response
        response = SimpleNamespace(data=None, errors=None)

        # ZMQ Request Body
        request_zmq = await node.recv()
        request_head = request_zmq.head
        request_body = request_zmq.body

        # GraphQL
        query_string = request_body.get("query")
        if query_string:
            response = await app.schema.execute(
                query_string,
                context_value=request_head.get("context", {}),
                operation_name=request_body.get("operation"),
                variable_values=request_body.get("variables"),
            )

        # print("QUEUE-REQUEST")
        # print(request_zmq)
        # Send Response
        await node.send(
            {},
            data=response.data,
            errors=([str(err) for err in response.errors] if response.errors else None),
        )
