# Forwarder — `Pub` and `Sub`

In this guide, you'll learn how to implement `PUB/SUB` operations. Optionally, you can utilize the GraphQL schema to obtain information for publishing.

## `PUB` Operations

Must be inside a file named `publishers.py`

Publishers use the function's name as the default `channel` for clients to subscribe to. However, you have two options for customizing the channel:

1. **Specify the channel** in the decorator.
2. **Dynamically set** the channel in the response's **`meta`** within the function (**Not recommended**).

### Example

```python title="publishers.py"
@zmag.pub  # or zmag.pub(seconds=5)
async def topic():  # `topic` is the channel
    response = zmag.Data()
    response.body = {"message": "hello world"}
    return response

# GraphQL Query
@zmag.pub(channel="custom_name")
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
    response.meta["channel"] = "my_channel" # won't register
    response.body = {"message": "hello world"}
    return response
```

## Settings

```toml title="config/spoc.toml"
[spoc.zmq]
...
device = "forwarder"  # options: queue, forwarder, streamer
...
```

<!-- termynal -->

```
$ python main.py runserver
INFO    -  Starting Application . . .
```

## List Channels

If you set the channel name **dynamically**, it will not be registered in the channels list.

<!-- termynal -->

```
$ python main.py channels

— custom_name
— generic
— topic
```
