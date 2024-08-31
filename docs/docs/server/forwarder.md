# Forwarder — `Pub` and `Sub`

In this guide, you'll learn how to implement `PUB` operations. Optionally, you can utilize the GraphQL schema to obtain information for publishing.

## `PUB` Operations

Must be inside a file named `publishers.py`

Publishers use the function's name as the default `channel` for clients to subscribe to. However, you have two options for customizing the channel:

1. **Specify the channel in the decorator.**
2. **Dynamically set the channel in the response's metadata within the function.**

### Example

```python title="publishers.py"
@zmag.pub  # or zmag.pub(seconds=5)
async def topic():  # `topic` is the default channel
    response = zmag.Data()
    response.body = {"message": "hello world"}
    return response

# GraphQL Query
@zmag.pub(channel="change_name")
async def graphql(context):
    gql_query = "query { books { id title } }"
    results = await context.schema.execute(gql_query)
    response = zmag.Data()
    response.body = results.data
    return response

# Custom Channel
@zmag.pub(seconds=5)
async def generic():
    response = zmag.Data()
    response.meta["channel"] = "custom"
    response.body = {"message": "hello world"}
    return response
```

## Settings

```toml title="config/spoc.toml"
# ZeroMQ Configuration
[spoc.zmq]
...
device = "forwarder"  # options: queue, forwarder, streamer
...
```
