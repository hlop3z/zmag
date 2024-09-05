# Project Overview

```text

zmag/
|-- framework/
|   |-- apps_templates/         --> Built-in templates for applications
|   |-- commands/               --> CLI commands and utilities
|   |   |-- __init__.py
|   |   |-- cli.py              --> Main entry point for CLI and shell commands
|   |   |-- core_commands.py    --> Core server-related commands
|   |   |-- keypair.py          --> Keypair for ZeroMQ
|   |   |-- shell.py            --> Utility functions for CLI tools
|   |   `-- utils.py            --> Helper functions and banner imports
|   |-- components/             --> Core components of the framework
|   |   |-- handlers/           --> Handlers for various components
|   |   |   |-- graphql/        --> GraphQL-specific handlers
|   |   |   |   |-- __init__.py
|   |   |   |   |-- base.py     --> Handlers for GraphQL
|   |   |   |   `-- schema.py   --> Schema handler for GraphQL
|   |   |   |-- __init__.py
|   |   |   `-- utils.py        --> Utility functions for component handlers
|   |   |-- __init__.py
|   |   |-- base.py             --> Base for framework components
|   |   |-- commands.py         --> Bases for CLI and Command
|   |   |-- forms.py            --> Utilities for Forms
|   |   |-- graphql.py          --> Bases for GraphQL
|   |   |-- network.py          --> Bases for ZeroMQ
|   |   `-- objects.py          --> Utilities for objects
|   |-- services/               --> Services and background tasks
|   |   |-- __init__.py
|   |   |-- debugger.py         --> Debugging server
|   |   |-- pub_push.py         --> Publisher/Pusher server
|   |   |-- queue.py            --> Queue server
|   |   |-- runner.py           --> Task runner and management
|   |   `-- watcher.py          --> Watchers for file or process changes
|   |-- __init__.py
|   `-- framework.py            --> Core framework setup
|-- graphql/                    --> GraphQL-related tools and definitions
|   |-- __init__.py
|   |-- inputs.py               --> Input definitions for GraphQL queries and mutations
|   `-- types.py                --> Type definitions for GraphQL schema
|-- network/                    --> Core ZeroMQ functionalities
|   |-- __init__.py
|   |-- base.py                 --> Base ZeroMQ classes
|   |-- keypair.py              --> Keypair generator
|   `-- utils.py                --> Utility functions for network operations
|-- tools/                      --> Miscellaneous utility tools
|   |-- __init__.py
|   |-- coro.py                 --> Coroutine utilities
|   |-- generic.py              --> Generic helper functions
|   |-- text.py                 --> Text processing utilities
|   `-- timer.py                --> Timer and scheduling utilities
|-- __about__.py                --> Package metadata and information
|-- __init__.py
|-- external.py                 --> Attempt to import external modules
|-- py.typed                    --> Type hints support for the package
`-- types.py                    --> Generic type definitions

```
