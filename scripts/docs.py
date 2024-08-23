import os
from pathlib import Path

# Command(s) to Execute
cmd_dev = "cd docs/ && python -m mkdocs serve --dev-addr 0.0.0.0:8055"
cmd_deploy = "cd docs/ && python -m mkdocs gh-deploy --force"


if __name__ == "__main__":
    import argparse

    # Base Directory
    base_dir = Path(__file__).parents[1]

    # CLI
    parser = argparse.ArgumentParser(description="Docs Manager.")
    parser.add_argument("-gh", "--github", action="store_true", help="Deploy to Github")

    # Collect ARGs
    args = parser.parse_args()

    # Run Command
    if args.github:
        os.system(cmd_deploy)
    else:
        os.system(cmd_dev)
