# **Client** Introduction

To get started with the ZMAG client, first install the package:

```sh
python -m pip install "zmag"
```

---

## **Client Setup**

To create a client instance using the `Frontend` class, you need to specify the server address and mode.

```python
from zmag import Frontend

client = Frontend(
    host="tcp://127.0.0.1:5555",  # Define the host address
    mode="queue",  # Specify the messaging mode
    is_sync=True,  # Whether the client operates in synchronous mode
)
```

---

## **Synchronous Mode**

By setting `is_sync=True`, the client operates in synchronous mode, allowing the methods to run synchronously. By default, ZMAG operates asynchronously.

### **When to Use Sync Mode**

- **Django Integration**: Sync mode is useful when running the client within Django or any other framework that expects synchronous execution.
- **Testing**: Useful for simplifying test cases that don't require asynchronous execution.

---

## **Mode Options**

The `mode` parameter defines the communication pattern. The mode you choose must align with the mode in which the **server/backend** is configured.

- **`queue`**: For request-response communication.
- **`streamer`**: For push-pull messaging patterns.
- **`forwarder`**: For publish-subscribe messaging patterns.

Ensure the client’s `mode` matches the server’s to facilitate proper communication.

---

This setup provides flexibility based on the communication pattern you need.
