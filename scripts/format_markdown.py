#!/usr/bin/env python3
"""Format all .md and .mdx files in the repository using Prettier."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = ("*.md", "*.mdx")
EXCLUDE_DIRS = {"node_modules", ".git", "dist", ".docusaurus"}
BATCH_SIZE = 50


def main() -> int:
    files = []
    for ext in EXTENSIONS:
        for f in REPO_ROOT.rglob(ext):
            if not EXCLUDE_DIRS.intersection(f.relative_to(REPO_ROOT).parts):
                files.append(f)

    if not files:
        print("No .md/.mdx files found.")
        return 0

    print(f"Formatting {len(files)} file(s)...")
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i : i + BATCH_SIZE]
        result = subprocess.run(
            ["npx", "--yes", "prettier", "--write", "--prose-wrap", "preserve", *batch],
            cwd=REPO_ROOT,
            shell=True,
        )
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
