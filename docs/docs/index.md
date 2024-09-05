#

<div style="text-align:center; margin-top: -60px">
 <img src="assets/images/title.png" alt="Alt text" class="title-image" />
</div>

---

<p align="center" class="name-acronym" >
    {{ acronym("ZeroMQ") }} —
    {{ acronym("Manages") }} —
    {{ acronym("A") }} —
    {{ acronym("GraphQL") }}
</p>

---

<!-- termynal -->

```
$ python -m pip install "zmag[server]"
---> 100%
Successfully installed zmag!
```

---

**ZMAG** is a tool designed for building **network APIs** rather than traditional web applications, leveraging the unique combination of **GraphQL** and **ZeroMQ**. By integrating **GraphQL's** flexible and efficient querying capabilities with **ZeroMQ's** high-performance messaging patterns, **ZMAG** enables developers to create robust and scalable network APIs. This approach allows for real-time communication, seamless data transfer, and efficient management of complex, distributed systems, making **ZMAG** an ideal choice for developers looking to build sophisticated network services that go beyond the capabilities of standard web applications.

**ZMAG** is designed to provide a more Pythonic syntax, moving away from the typical GraphQL and ZeroMQ styles and focusing instead on native Python conventions for greater readability and intuitiveness.

!!! info "Capabilities of ZMAG"

    1. Build **GraphQL** **Queries** and **Mutations** for flexible data interactions.
    2. Develop **Request** and **Response** APIs for efficient communication.
    3. Implement **Pub/Sub** and **Push/Pull** patterns for robust messaging and data distribution.
    4. Leverage **Commands** to automate processes and streamline operations.

---

## Built With

| Module                                         | Purpose                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| [**pyzmq**](https://pyzmq.readthedocs.io)      | Core **Universal Messaging Library** for the API.                  |
| [**orjson**](https://github.com/ijl/orjson)    | Fast Python JSON library.                                          |
| [**strawberry**](https://strawberry.rocks/)    | **GraphQL Library**                                                |
| [**click**](https://github.com/pallets/click/) | Manage the server, development processes, and custom **Commands**. |
| [**spoc**](https://pypi.org/project/spoc/)     | **Framework tool** for building this framework.                    |

## Debug Server Built With

| Module                                                   | Purpose                               |
| -------------------------------------------------------- | ------------------------------------- |
| [**starlette**](https://www.starlette.io/)               | Runs the server in **Debug** mode.    |
| [**uvicorn**](https://www.uvicorn.org/)                  | ASGI web server.                      |
| [**watchdog**](https://github.com/gorakhargosh/watchdog) | Restarts the debug server on changes. |

---

## Installation

To install **ZMAG** in different environments, use the following commands:

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

!!! warning

    ZMAG is currently in its early stages of development, so there may be some changes in the future. However, we aim to keep the public API stable.

---

## Project **Flowchart**

| **(API)** Application Programming Interface | **(CLI)** Command-Line Interface     |
| ------------------------------------------- | ------------------------------------ |
| 1. Load all **`Settings`**.                 | 1. Load all **`Settings`**.          |
| 2. Load **`Environment Variables`**.        | 2. Load **`Environment Variables`**. |
| 3. Load all **`Apps` (Packages)**.          | 3. Load all **`Apps` (Packages)**.   |
| 4. Start the **`ZeroMQ`** **API**           | 4. Start the **`CLI`** **Manager**.  |

```mermaid
flowchart LR;
    subgraph ZMAG & Installed Apps
    A --> B;

    B <--> D;
    B <--> E;
    end

    D <--> F;
    E <--> G;

    subgraph Your Code
    F <--> | GraphQL | H
    G <--> | GraphQL | H
    end

    A{Click};
    B[Settings & Apps];
    D{The API};
    E{The CLI};
    F((Operations))
    G((Commands))
    H{Project};
```

### Explanation

The flowchart illustrates how the project initializes and operates both the **API** and **CLI** interfaces:

1. **Initialization**: The process begins with **Click**, which is used to launch both the API (services) and CLI (commands).
2. **Configuration Loading**: For both the API and CLI interfaces, all **`Settings`**, **`Environment Variables`**, and **`Apps (Modules)`** are loaded. This ensures the environment is properly configured and all necessary modules are available.

3. **Starting Interfaces**:

    !!! Note "Interfaces"

         - **API** — the **ZeroMQ Backend** is started to manage backend processes and facilitate operations.
         - **CLI** — the **CLI Manager** is initiated using Click, which handles command-line inputs and operations.

4. **Integration with GraphQL**: Both the **API** and **CLI** interfaces can connect to the **GraphQL**, allowing you to perform GraphQL operations through either the **API** or the **CLI**.

5. **Custom Extensions**: You have the flexibility to create custom **CLI** commands or **API** methods, which can leverage the underlying **GraphQL** capabilities.

!!! tip

    The setup provides a versatile and unified framework, enabling you to manage backend processes and handle command-line operations effectively, with seamless integration of GraphQL functionalities across both interfaces.

---

## Architectural **Patterns**

These patterns illustrate the flow of communication in a zmag system:

### Backend — Frontend

A direct communication pattern where the Backend communicates with the Frontend.

```mermaid
flowchart LR;
    A[Backend] <--> B[Frontend];
```

### Backend — Device — Frontend

An intermediary device manages the communication between the Backend and Frontend, allowing for scalability.

```mermaid
flowchart LR;
    A[Backend] <--> B((Device)) <--> C[Frontend];
    F[Backend] <--> B <--> D[Frontend];
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

**ZMAG** comes with several key commands:

| Command               | Purpose                                                 |
| --------------------- | ------------------------------------------------------- |
| `zmag-init`           | Create a new **ZMAG** project.                          |
| `./main.py runserver` | Run the **Server**.                                     |
| `./main.py start-app` | Create a **ZMAG App** inside your **`apps`** directory. |
| `./main.py --help`    | Display more information about available commands.      |

!!! warning "Important: `zmag-init` Command"

    Use the `zmag-init` command **only once** and make sure you are in a **new folder**. This command will write files and folders to the current directory.
