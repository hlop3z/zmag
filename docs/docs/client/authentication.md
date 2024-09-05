# **Authentication**

ZMAG provides multiple ways to authenticate your client, either via **Keys** or through **SSH** configuration.

---

## **Authentication via Keys**

To authenticate using keys, pass the `publickey`, `secretkey`, and `serverkey` directly to the `Frontend` instance.

```python
from zmag import Frontend

client = Frontend(
    publickey="public-key-x7i+CS<BVZMJyXEX)H8?31k5o)?mQ",  # Client's public key
    secretkey="secret-key-x(<$ES*$pZ3UmIPEIy+lt1qNY!!Kn",  # Client's secret key
    serverkey="server-key-QAvkkf}^Y5OVu=R?S<V9Xi-Y!Zm4q",  # Server's public key
)
```

### **Key Details**

- **Public Key**: Identifies your client.
- **Secret Key**: Authenticates your client to the server.
- **Server Key**: The public key of the server you are connecting to.

### **Generate Key Pair**

```python
import zmag

publickey, secretkey = zmag.keypair()
```

---

## **Authentication via SSH**

Alternatively, you can authenticate via SSH by passing an SSH configuration using `ConfigSSH`.

```python
from zmag import Frontend, ConfigSSH

client = Frontend(
    ssh=ConfigSSH(
        host="user@server:port",  # Specify the SSH host and port
        keyfile="key/file/path",  # Path to the SSH private key file
    )
)
```

### **SSH Configuration**

- **Host**: Specifies the user, server, and port in the format `user@server:port`.
- **Keyfile**: The path to your SSH private key file used for authentication.

---

By choosing between key-based or SSH-based authentication, you can securely configure your client based on your application’s needs.
