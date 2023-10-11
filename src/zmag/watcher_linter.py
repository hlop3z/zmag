#!/usr/bin/env python
async def watch_linter():
    import asyncio
    import subprocess
    import watchgod
    from pathlib import Path

    # FrameWork
    from .framework import Framework

    app = Framework()

    regex = r"^.*(\.py)$"
    base_dir = app.base_dir  # Path(__file__).resolve().parents[1]

    # Tools
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

    watch_src = asyncio.create_task(change_handler(base_dir, regex, handler=handler))

    return watch_src
