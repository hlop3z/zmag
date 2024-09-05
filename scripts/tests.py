import subprocess
from pathlib import Path
import argparse
import os
import signal

# Define the commands
cmd_server = "python main.py"
cmd_client = "python client.py"
cmd_device = "python device.py"

GLOBAL_WORKERS = {}


def signal_handler(sig, frame):
    # Terminate
    for process in GLOBAL_WORKERS.values():
        try:
            process.terminate()
        except Exception:
            pass

    # Kill Processes
    for pid in GLOBAL_WORKERS.keys():
        try:
            os.kill(pid, signal.SIGINT)
        except Exception:
            pass


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def execute_command(
    the_dir: Path, command: str, params: str = "", timeout: int | None = None
):
    """Execute a shell command with optional parameters."""
    full_command = f"{command} {params}".strip()
    try:
        # Optional: Print the command being executed
        print(f"Executing: {full_command}\n")
        # subprocess.run(full_command, cwd=the_dir, shell=True, check=True)
        process = subprocess.Popen(
            full_command,
            cwd=the_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # This argument makes the output streams text instead of bytes (Python 3.7+)
            bufsize=1,  # Line-buffered output for real-time reading
        )

        # Register Process
        GLOBAL_WORKERS[process.pid] = process

        # Read stdout and stderr line-by-line in real-time
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line, end="")  # Print the stdout line immediately

        for stderr_line in iter(process.stderr.readline, ""):
            print(stderr_line, end="")  # Print the stderr line immediately

        # Wait for the process to complete
        process.stdout.close()
        process.stderr.close()
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")
    except KeyboardInterrupt:
        pass
    finally:
        signal_handler(None, None)


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
