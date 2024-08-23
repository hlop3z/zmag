import os
from pathlib import Path

# Command(s) to Execute
cmd_server = "cd tests/server && python main.py"
cmd_client = "cd tests/client && python client.py"


if __name__ == "__main__":
    import argparse

    # Base Directory
    base_dir = Path(__file__).parents[1]

    # CLI
    parser = argparse.ArgumentParser(description="Test Manager.")
    parser.add_argument("-c", "--client", action="store_true", help="Test Client")
    parser.add_argument("-s", "--server", action="store_true", help="Test Server")
    parser.add_argument("-a", "--args", nargs="+", help="A list of options")

    # Collect ARGs
    args = parser.parse_args()

    # Run Command
    if args.client:
        os.system(cmd_client)
    else:
        params = " ".join(args.args or [])
        os.system(f"{cmd_server} {params}")
