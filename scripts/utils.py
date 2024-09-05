from pathlib import Path
import argparse

FOLDERS_TO_IGNORE = ["__pycache__"]
FILES_TO_IGNORE = []


def print_tree(root_dir: Path, prefix: str = "", is_root: bool = True):
    """Recursively prints the directory tree structure with directories listed before files."""
    if is_root:
        print(root_dir.name + "/")

    try:  # Get the list of all entries in the directory
        entries = list(root_dir.iterdir())
    except PermissionError:
        return  # Skip directories where permission is denied

    # Separate directories and files
    directories = [
        entry
        for entry in entries
        if entry.is_dir() and entry.name not in FOLDERS_TO_IGNORE
    ]
    files = [
        entry
        for entry in entries
        if entry.is_file() and entry.name not in FILES_TO_IGNORE
    ]

    # Sort directories and files
    directories.sort(key=lambda x: x.name)
    files.sort(key=lambda x: x.name)

    # Print directories
    for index, entry in enumerate(directories):
        is_last_entry = index == len(directories)
        connector = "`-- " if is_last_entry else "|-- "
        print(prefix + connector + entry.name + "/")
        new_prefix = prefix + ("    " if is_last_entry else "|   ")
        print_tree(entry, new_prefix, False)

    # Print files
    for index, entry in enumerate(files):
        is_last_entry = index == len(files) - 1
        connector = "`-- " if is_last_entry else "|-- "
        print(prefix + connector + entry.name)


def main():
    # Base Directory
    base_dir = Path(__file__).parents[1]

    # CLI
    parser = argparse.ArgumentParser(description="Test Manager.")
    parser.add_argument("--tree", action="store_true", help="Print folder tree")
    parser.add_argument(
        "-a",
        "--args",
        nargs=argparse.REMAINDER,
        help="Additional arguments for the command",
    )

    # Parse arguments
    args = parser.parse_args()

    # Determine which command to run
    if args.tree:
        print_tree(base_dir / args.args[0])


if __name__ == "__main__":
    main()
