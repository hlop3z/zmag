# `Queue`

In this guide, you'll learn how to run the server in `Request/Response` mode. To create operations for the `Queue` mode look at [GraphQL Operations](/{{ url("/server/graphql/operations/") }}).

Here will learn how to configure the server to run on Queue mode which its very simple set the **`device`** to **`queue`**

## Settings

```toml title="config/spoc.toml"
[spoc.zmq]
...
device = "queue"  # options: queue, forwarder, streamer
...
```

<!-- termynal -->

```
$ python main.py runserver
INFO    -  Starting Application . . .
```
