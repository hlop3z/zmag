# Welcome to **{{ config.site_name }}**

---

**(Z)**eroMQ **(M)**anages — **(A)** — **(G)**raphQL

---

**{{ config.site_name }}** is a tool designed for building **network APIs** rather than traditional web applications, leveraging the unique combination of **GraphQL** and **ZeroMQ**. By integrating **GraphQL's** flexible and efficient querying capabilities with **ZeroMQ's** high-performance messaging patterns, **{{ config.site_name }}** enables developers to create robust and scalable network APIs. This approach allows for real-time communication, seamless data transfer, and efficient management of complex, distributed systems, making **{{ config.site_name }}** an ideal choice for developers looking to build sophisticated network services that go beyond the capabilities of standard web applications.

!!! info "Capabilities of {{ config.site_name }}"

    1. Build **GraphQL** **Queries** and **Mutations** for flexible data interactions.
    2. Develop **Request** and **Response** APIs for efficient communication.
    3. Implement **Pub/Sub** and **Push/Pull** patterns for robust messaging and data distribution.
    4. Leverage **Commands** to automate processes and streamline operations.

<!-- termynal -->

```
$ show progress
---> 100%
Done!
```

---

## Built With

| Module                                         | Purpose                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| [**Pyzmq**](https://pyzmq.readthedocs.io)      | Core **Universal Messaging Library** for the API.                  |
| [**Strawberry**](https://strawberry.rocks/)    | **GraphQL Library**                                                |
| [**Click**](https://github.com/pallets/click/) | Manage the server, development processes, and custom **Commands**. |
| [**SPOC**](https://pypi.org/project/spoc/)     | **Framework tool** for building this framework.                    |

## Debug Server Built With

| Module                                                   | Purpose                               |
| -------------------------------------------------------- | ------------------------------------- |
| [**Starlette**](https://www.starlette.io/)               | Runs the server in **Debug** mode.    |
| [**Uvicorn**](https://www.uvicorn.org/)                  | ASGI web server.                      |
| [**Watchdog**](https://github.com/gorakhargosh/watchdog) | Restarts the debug server on changes. |

---

## Installation

To install **{{ config.site_name }}** in different environments, use the following commands:

### **Development** Environment

```sh
python -m pip install "zmag[debug,server]"
```

### **Server** Environment

```sh
python -m pip install "zmag[server]"
```

### **Client** Environment

```sh
python -m pip install "zmag"
```

---

## Core **Layout**

```text
root/                           --> <Directory> - Project's Root
|
|-- apps/                       --> <Directory> - Project's Apps
|
|-- config/                     --> <Directory> - Configurations
|    |-- .env                   --> <Directory> - Environment Settings
|    |-- ...
|    |-- settings.py            --> <File> - Pythonic API Settings
|    `-- spoc.toml              --> <File> - TOML API Settings
|
`-- etc...
```

---

## Key Commands

**{{ config.site_name }}** comes with several key commands:

| Command                               | Purpose                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------- |
| `{{ config.site_name.lower() }}-init` | Create a new **{{ config.site_name }}** project.                          |
| `./main.py run`                       | Run the **Server**.                                                       |
| `./main.py start-app`                 | Create a **{{ config.site_name }} App** inside your **`apps`** directory. |
| `./main.py --help`                    | Display more information about available commands.                        |

!!! warning "Important: `startproject` Command"

    Use the `startproject` command **only once** and make sure you are in a **new folder**. This command will write files and folders to the current directory.
