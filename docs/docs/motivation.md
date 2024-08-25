# Motivation

Network applications are software programs that run on multiple computers and devices connected over a network (such as a local area network (LAN), a wide area network (WAN), or the internet). These applications are designed to interact with a network to provide specific functionalities, such as file sharing, messaging, database access, or remote management.

!!! warning

    ZMAG is currently in its early stages of development, so there may be some changes in the future. However, we aim to keep the public API stable.

**Key Characteristics**:

1. **Direct Communication**: Network applications often use protocols like TCP/IP to communicate directly over a network. Examples include FTP clients, email clients, and peer-to-peer (P2P) applications.
2. **Low Latency**: Network applications typically have lower latency due to direct communication over the network, which is crucial for real-time applications such as video conferencing, online gaming, and financial trading systems.
3. **Complex Configuration**: They often require more complex setup and configuration, especially when dealing with network security, firewalls, and access permissions.
4. **Offline Capabilities**: Some network applications can work offline and synchronize data when a network connection is reestablished, making them reliable in scenarios where connectivity is intermittent.

**Advantages**:

- **Performance**: Faster communication and data transfer speeds due to direct network connections.
- **Security**: Potentially more secure because they can operate within a private network environment.
- **Control and Customization**: Greater control over the network environment and application customization based on specific organizational needs.

**Example Use Cases**:

- **Enterprise Resource Planning (ERP)** systems that require robust, secure internal network communications.
- **Local Database Applications** where performance and data security are critical.

---

### **`Network`** vs **`Web`** Applications — Comparison Summary

| Feature                  | Network Applications                                                  | Web Applications                                             |
| ------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Accessibility**        | Limited to network-connected devices                                  | Accessible from any device with a browser                    |
| **Installation**         | Requires installation on each device                                  | No installation required                                     |
| **Updates**              | May require individual updates or patches                             | Centralized updates on the server                            |
| **Performance**          | Generally faster with lower latency due to direct network connections | Dependent on internet speed and server load                  |
| **Security**             | Can be more secure within a private network                           | Security relies on web standards and protocols (HTTPS, etc.) |
| **Offline Capabilities** | Often available                                                       | Limited (except for PWAs)                                    |
| **Development**          | More complex setup and configuration                                  | Simpler to develop and deploy using web technologies         |
| **Scalability**          | May require significant resources for scaling                         | Easily scalable on cloud infrastructure                      |
| **Customization**        | Highly customizable within the network environment                    | Customization often limited to web technologies              |
