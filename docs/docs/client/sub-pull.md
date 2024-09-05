# **`Subscribe`** and **`Pull`** in ZMAG

These examples demonstrate how to use the `Frontend` class in ZMAG for subscribing to channels and pulling work from a server.

```python
from zmag import Frontend

client = Frontend(
    host="tcp://127.0.0.1:5555",
    mode="queue",
    is_sync=False,  
)
```

---

## **Subscribe**

The `subscribe` method is used to listen for messages from specific channels.

### **Subscribe to All Channels**

Subscribing with an empty string (`""`) listens to messages from all channels.

```python
while True:
    message = await client.subscribe("")
    print("Received:", message)
```

### **Subscribe to a Specific Channel**

To limit the subscription to a particular channel, pass the channel name as an argument.

```python
while True:
    message = await client.subscribe("the_channel")
    print("Received:", message)
```

---

## **Pull**

The `pull` method is used to receive work from a push-pull pattern (also known as task distribution).

```python
while True:
    work = await client.pull()
    print("Received:", work)
```
