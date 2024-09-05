# ZMAG **Limitations**

**ZMAG** is not intended to function as a full-fledged GraphQL endpoint, particularly in the context of HTTP-based GraphQL features such as subscriptions and federations. Instead, **ZMAG** is designed to generate self-documenting Python code that offers significant flexibility in the types of output you can request from your operations.

The core functionality of **ZMAG** revolves around **ZeroMQ**, with **GraphQL** serving primarily as a convenient means to interact with ZeroMQ. The primary design philosophy behind **ZMAG** is to be as Pythonic as possible, focusing on creating classes and functions that can be used remotely. The use of GraphQL is supplementary, facilitating the integration with ZeroMQ rather than serving as the main feature.

In summary, **ZMAG** leverages GraphQL for its convenience but is fundamentally centered around **ZeroMQ** and **Pythonic** design principles.
