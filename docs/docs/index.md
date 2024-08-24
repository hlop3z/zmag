# Welcome to **ZMAG**

---

**(Z)**eroMQ **(M)**anages — **(A)** — **(G)**raphql

---

**ZMAG** is a powerful tool designed for building **network APIs** rather than traditional web applications, leveraging the unique combination of **GraphQL** and **ZeroMQ**. By integrating **GraphQL's** flexible and efficient querying capabilities with **ZeroMQ's** high-performance messaging patterns, **ZMAG** enables developers to create robust and scalable network APIs. This approach allows for real-time communication, seamless data transfer, and efficient management of complex, distributed systems, making **ZMAG** an ideal choice for developers looking to build sophisticated network services that go beyond the capabilities of standard web applications.

!!! info "Capabilities of ZMAG"

    1. Build **GraphQL** **Queries** and **Mutations** for flexible data interactions.
    2. Develop **Request** and **Response** APIs for efficient communication.
    3. Implement **Pub/Sub** and **Push/Pull** patterns for robust messaging and data distribution.
    4. Leverage **Commands** to automate processes and streamline operations.

<div id="terminal-index" data-termynal></div>

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

To install **Zmag** in different environments, use the following commands:

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

**Zmag** comes with several key commands:

| Command               | Purpose                                                 |
| --------------------- | ------------------------------------------------------- |
| `startproject`        | Create a new **ZMAG** project.                          |
| `./main.py run`       | Run the **Server**.                                     |
| `./main.py start-app` | Create a **Zmag App** inside your **`apps`** directory. |
| `./main.py --help`    | Display more information about available commands.      |

!!! warning "Important: `startproject` Command"

    Use the `startproject` command **only once** and make sure you are in a **new folder**. This command will write files and folders to the current directory.
