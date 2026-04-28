import json
import os
import platform
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
MCP_JSON_FILE = ".mcp.json"


def npx_command(package: Any, extra_args: Any = None) -> Any:
    extra_args = extra_args or []
    system = platform.system().lower()

    if system == "windows":
        return {"command": "cmd", "args": ["/c", "npx", "-y", package, *extra_args]}
    else:
        return {"command": "npx", "args": ["-y", package, *extra_args]}


def generate_config(project_root: Any) -> Any:
    return {
        "mcpServers": {
            "filesystem": npx_command(
                "@modelcontextprotocol/server-filesystem", [str(project_root)]
            ),
            "context7": npx_command("@upstash/context7-mcp"),
            "basic-memory": {"command": "uvx", "args": ["basic-memory", "mcp"]},
            "sequential-thinking": npx_command(
                "@modelcontextprotocol/server-sequential-thinking"
            ),
        }
    }


def main():
    output_file = REPO_ROOT / MCP_JSON_FILE
    config_string = generate_config(REPO_ROOT)

    with open(output_file, "w") as f:
        json.dump(config_string, f, indent=2)

    try:
        os.chmod(output_file, 0o600)
    except Exception:
        pass

    print(f"MCP config written to: {output_file}")
    print(f"Filesystem access limited to: {REPO_ROOT}")
    print(f"Detected OS: {platform.system()}")


if __name__ == "__main__":
    main()
