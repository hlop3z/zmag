#!/usr/bin/env python

import asyncio
import subprocess
import watchgod
from pathlib import Path


def shell_cmd(name=None, cmd=None, check=True):
    print(f"Running... <{name}>")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        print(f"Error while running {name}")


async def change_handler(path=None, regex=None, handler=None):
    async for changes in watchgod.awatch(
        path,
        watcher_cls=watchgod.RegExpWatcher,
        watcher_kwargs=dict(re_files=regex),
    ):
        for change in changes:
            method, path = change
            if handler:
                handler(Path(path))


def handler(path):
    print(f"Fixing... {path}")
    shell_cmd("isort", f'python -m isort --profile black "{path}"')
    shell_cmd("black", f'python -m black "{path}"')


async def main():
    regex = r"^.*(\.py)$"
    base_dir = Path(__file__).resolve().parents[1]

    watch_src = asyncio.create_task(
        change_handler(base_dir / "src", regex, handler=handler)
    )
    watch_tests = asyncio.create_task(
        change_handler(base_dir / "tests", regex, handler=handler)
    )

    await asyncio.gather(watch_src, watch_tests)


if __name__ == "__main__":
    asyncio.run(main())
