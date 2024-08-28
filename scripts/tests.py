import subprocess
from pathlib import Path
import argparse

# Define the commands
cmd_server = "python main.py"
cmd_client = "python client.py"
cmd_device = "python device.py"


def execute_command(the_dir: Path, command: str, params: str = ""):
    """Execute a shell command with optional parameters."""
    try:
        full_command = f"{command} {params}".strip()
        # Optional: Print the command being executed
        print(f"Executing: {full_command}\n")
        subprocess.run(full_command, cwd=the_dir, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")


def main():
    # Base Directory
    base_dir = Path(__file__).parents[1]
    test_dir = base_dir / "tests"

    # CLI
    parser = argparse.ArgumentParser(description="Test Manager.")
    parser.add_argument("-c", "--client", action="store_true", help="Run Client Test")
    parser.add_argument("-s", "--server", action="store_true", help="Run Server Test")
    parser.add_argument("-d", "--device", action="store_true", help="Run Device Test")
    parser.add_argument(
        "-a",
        "--args",
        nargs=argparse.REMAINDER,
        help="Additional arguments for the command",
    )

    # Parse arguments
    args = parser.parse_args()

    # Determine which command to run
    if args.client:
        execute_command(test_dir / "client", cmd_client)
    elif args.device:
        execute_command(test_dir / "device", cmd_device)
    elif args.server:
        params = " ".join(args.args or [])
        execute_command(test_dir / "server", cmd_server, params)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
