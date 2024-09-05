# Streamer — `Push` and `Pull`

In this guide, you'll learn how to implement `PUSH/PULL` operations. Optionally, you can utilize the GraphQL schema to obtain information for pushing.

## `PUSH` Operations

Must be inside a file named `pushers.py`

Pushers operate similarly to publishers, but they do not use channels. Instead, the workload is distributed using a **round-robin** load balancing algorithm.

### Example

```python title="pushers.py"

@zmag.push
async def task_one(context):
    gql_query = "query { books { id title } }"
    results = await context.schema.execute(gql_query)
    response = zmag.Data()
    response.body = results.data
    return response

@zmag.push(seconds=5)
async def task_two():
    response = zmag.Data()
    response.body = {"message": "hello world"}
    return response
```

## Settings

```toml title="config/spoc.toml"
[spoc.zmq]
...
device = "streamer"  # options: queue, forwarder, streamer
...
```

<!-- termynal -->

```
$ python main.py runserver
INFO    -  Starting Application . . .
```

## List Tasks

The task will be displayed as `<app_name>.<task_name>(time = <time_in_seconds>)`.

<!-- termynal -->

```
$ python main.py tasks

— demo.task_one(time=0)
— demo.task_two(time=5)

```
