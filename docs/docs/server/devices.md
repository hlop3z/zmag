# Devices

ZeroMQ devices are specialized components provided by the ZeroMQ messaging library to facilitate complex messaging patterns. They serve as intermediaries that handle specific messaging tasks, such as forwarding messages between different types of sockets, proxying, and load balancing. Devices simplify the creation of advanced messaging workflows by managing the intricacies of message routing and handling.

## Purpose

1. **Message Forwarding**: Efficiently routes messages between different sockets.
2. **Proxying**: Acts as an intermediary to manage communication between various endpoints.
3. **Load Balancing**: Distributes messages evenly across multiple workers.

## Types of Devices

- **`Queue`**: Implements `Request/Response` patterns, handling message queues.
- **`Forwarder`**: Implements `Publish/Subscribe` patterns, forwarding messages between publishers and subscribers.
- **`Streamer`**: Implements `Push/Pull` patterns, managing the flow of messages between producers and consumers.

## Advantages

- **Abstraction**: Devices abstract complex message routing and handling, simplifying application development.
- **Scalability**: Supports scalable and flexible messaging patterns, accommodating various use cases and architectures.
- **Efficiency**: Optimized for high-throughput and low-latency messaging, ensuring performance.

## Usage

Using ZeroMQ devices is optional. However, if your application requires multiple servers or workers, employing a device becomes necessary. ZMAG provides support for both scenarios. You can control whether a device is used and its configuration through settings:

- **Starting a Device**: Set `proxy = true` if the device runs within the application.

!!! note "Starting a Device"

    - `proxy = true`

- **Attaching to Device**: If the device is running in a separate environment, set `proxy = false` and `attach = true`.

!!! note "Attaching to Device"

    - `proxy = false`
    - `attach = true`

- **Running a Single Server**: If you want to run a single server without a device, set `proxy = false`, `attach = false`, and `workers = 1`.

!!! note "Single Server"

    - `workers = 1`
    - `proxy = false`
    - `attach = false`

## Settings

**Example Configuration:**

```toml title="config/spoc.toml"
# ZeroMQ Configuration
[spoc.zmq]
...
workers = 2
proxy = true
attach = true
...
```

By leveraging ZeroMQ devices, you can build robust and efficient messaging systems tailored to your application's needs.

---
