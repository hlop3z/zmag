# Environments

The following settings are used to configure your application for different environments such as `development`, `staging`, and `production`. Each environment has its own configuration file that specifies environment-specific settings.

```python
from spoc import settings

settings.ENV
```

## Settings **Locations**

The configuration files for different environments are organized under the `config` directory, specifically within the `.env` subdirectory. This structure helps to keep environment-specific settings separate and easily manageable.

```text
root/
|-- config/                      --> <Directory> - Configurations.
|    |-- ...
|    |-- .env/                   --> <Directory> - Environments.
|    |   |-- development.toml    --> <File> - Development Environment Settings.
|    |   |-- production.toml     --> <File> - Production Environment Settings.
|    |   `-- staging.toml        --> <File> - Staging Environment Settings.
|    `-- ...
`-- etc...
```

### Explanation

- **development.toml**: Contains settings specific to the development environment, such as debug configurations, development database connections, and more.
- **production.toml**: Holds settings tailored for the production environment, including optimized configurations for performance, security, and live data handling.
- **staging.toml**: Used for staging environments to mimic the production environment as closely as possible while allowing for final testing and validation.

## Key Sections

- **`[env]`**: General environment settings that apply to the current environment.
- **`[env.zmq]`**: Configuration specific to ZeroMQ.

## Development

The `development.toml` file is used to configure settings for the development environment. This typically includes settings that are more permissive and allow for debugging and testing during development.

```toml title="config/.env/development.toml"
[env] # Environment Settings

[env.zmq] # ZeroMQ Configuration
public_key = "public-key-x7i+CS<BVZMJyXEX)H8?31k5o)?mQ"
secret_key = "secret-key-x(<$ES*$pZ3UmIPEIy+lt1qNY!!Kn"
server_key = "server-key-QAvkkf}^Y5OVu=R?S<V9Xi-Y!Zm4q"
```

## Staging

The `staging.toml` file configures the staging environment, which is used for testing the application in a production-like setting without affecting the live environment. It often mirrors production settings with minor adjustments.

```toml title="config/.env/staging.toml"
[env] # Environment Settings ...
```

## Production

The `production.toml` file includes settings optimized for the live production environment. This configuration emphasizes security, performance, and stability to ensure the application runs smoothly in a live setting.

```toml title="config/.env/production.toml"
[env] # Environment Settings ...
```

---

## Summary

By organizing environment-specific settings into distinct files, you can easily switch between configurations for `development`, `staging`, and `production`. This structure also ensures that sensitive information, such as keys and environment variables, is properly managed and isolated per environment.
