# Settings

The following settings control the configuration of your ZMAG application, including installed apps, extra options, and specific configurations for different environments.

```python
from spoc import settings

print(settings.__dir__())
```

## Settings **Locations**

```text
root/
|--  config/                    --> <Directory> - Configurations.
|    |-- ...
|    |-- settings.py            --> <File> - Pythonic Settings.
|    `-- spoc.toml              --> <File> - Spoc Settings.
`-- etc...
```

## Python

| Key                  | Description                                                                             |
| -------------------- | --------------------------------------------------------------------------------------- |
| **`INSTALLED_APPS`** | A list of ZMAG **`apps`** that are currently **enabled** and in use within the project. |
| **`EXTRAS`**         | Additional **`components`** for the application.                                        |

### `settings.py`

Below is an example of a Python settings file (`settings.py`) used to configure your ZMAG project.

```python title="config/settings.py"
# -*- coding: utf-8 -*-
"""
    { Settings }
"""

import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]  # (1)

# Installed APPS
INSTALLED_APPS = ["app_one", "app_two"]  # (2)

# Additional Components
EXTRAS = {  # (3)
    "extensions": [],
    "permissions": [],
    "on_startup": [],
    "on_shutdown": [],
}
```

1. **Base Directory**: Defines the root directory of the project, setting the base path for all file operations.
2. **INSTALLED_APPS**: Specifies the ZMAG applications that are currently installed and active in the project.
3. **EXTRAS**: Defines additional configurations, including extensions, permissions, and event handlers for startup and shutdown.

## TOML

The `spoc.toml` file provides a declarative way to configure different aspects of your ZMAG project, from operating modes to specific settings for GraphQL and ZeroMQ.

| Key                           | Group     | Description                                                                                                  |
| ----------------------------- | --------- | ------------------------------------------------------------------------------------------------------------ |
| **`mode`**                    | `n/a`     | Specifies the environment mode for the application, such as (`development`, `production`, or `staging`).     |
| **`debug`**                   | `n/a`     | Enables or disables debug mode for the server, providing more detailed error messages and live reloading.    |
| **`authentication`**          | `n/a`     | Determines if authentication is required for both `frontend` and `backend` in ZeroMQ communications.         |
| **`max_depth`**               | `graphql` | Sets the maximum allowed depth for nested objects in a GraphQL query to control query complexity.            |
| **`introspection`**           | `graphql` | Enables querying of the current API schema to discover available resources and their structures.             |
| **`items_per_page`**          | `graphql` | Defines the maximum number of items returned per page in paginated GraphQL responses.                        |
| **`workers`**                 | `zmq`     | Specifies the number of worker processes or threads to handle ZeroMQ messaging tasks.                        |
| **`proxy`**                   | `zmq`     | Indicates whether to start a ZMQ proxy/broker `device` for message routing.                                  |
| **`attach`**                  | `zmq`     | Determines if the server should be attached to a ZMQ proxy/broker `device` for message forwarding.           |
| **`thread`**                  | `zmq`     | Configures whether to use threads or processes for ZeroMQ worker operations.                                 |
| **`device`**                  | `zmq`     | Specifies the messaging pattern to use (`queue`, `forwarder`, or `streamer`) within ZeroMQ.                  |
| **`server`** and **`client`** | `zmq`     | Defines the connection strings for the ZeroMQ server and client endpoints.                                   |
| **`permissions`**             | `extras`  | Lists the permission classes that control access to different parts of the application.                      |
| **`extensions`**              | `extras`  | Specifies the GraphQL extensions to enhance the API's functionality, such as custom directives or resolvers. |
| **`apps`**                    | `apps`    | Lists the installed apps for each environment mode, allowing customization of active apps per mode.          |

### `spoc.toml`

Here is an example of a `spoc.toml` configuration file:

```toml title="config/spoc.toml"
# Server Configuration
[spoc]
mode = "development"  # options: production, development, staging
debug = true
authentication = false

# GraphQL Configuration
[spoc.graphql]
max_depth = 4
introspection = true
items_per_page = 100

# ZeroMQ Configuration
[spoc.zmq]
workers = 1
proxy = true
attach = true
thread = false
device = "forwarder"  # options: queue, forwarder, streamer
server = "tcp://127.0.0.1:5556"
client = "tcp://127.0.0.1:5555"

# Installed Apps by Mode
[spoc.apps]
production = ["app_one"]
development = ["app_two", "app_three"]
staging = ["app_four"]

# Additional Components
[spoc.extras]
# Plugins
extensions = ["my_app.extensions.MyExtension"]
permissions = ["my_app.permissions.MyPermission"]

# Event Hooks
on_startup = ["my_app.events.on_startup"]
on_shutdown = ["my_app.events.on_shutdown"]
```

**Explanations**:

- **mode**: Specifies the running environment, allowing for different configurations in development, staging, or production.
- **GraphQL Settings**: Controls aspects of GraphQL, such as query depth and pagination limits.
- **ZeroMQ Settings**: Configures the messaging patterns and server/client details for ZeroMQ operations.
- **Apps and Extras**: Define which apps and additional features are enabled based on the current mode and user-defined settings.
- **Event Hooks**: Allows specification of functions that should run on startup and shutdown, enabling custom initialization and cleanup logic.
