import os
import asyncio
import multiprocessing

import click

server_process = []  # Global variable to hold the server process


def watcher(path_to_watch, functions, banner="Restarting Server ..."):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    restart_event = asyncio.Event()

    async def watch_directory(path_to_watch, on_modified):
        observer = Observer()
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified
        observer.schedule(event_handler, path=path_to_watch, recursive=True)
        observer.start()
        try:
            while True:
                await asyncio.sleep(1)  # Add a short sleep to avoid a busy loop
        finally:
            observer.stop()
            observer.join()

    def on_file_change(event):
        restart_event.set()  # Signal to restart the service

    async def restart_server():
        global server_process

        while True:
            await restart_event.wait()  # Wait for the event to be set
            restart_event.clear()  # Clear the event flag

            if len(server_process) > 0:
                for process in server_process:
                    process.terminate()
                    process.join()

            server_process = [multiprocessing.Process(**func) for func in functions]
            for process in server_process:
                process.start()

            await asyncio.sleep(5)
            click.clear()
            click.secho(f"{ banner }", fg="magenta", bold=True)

    async def main():
        watch_task = asyncio.create_task(watch_directory(path_to_watch, on_file_change))
        restart_task = asyncio.create_task(restart_server())

        restart_event.set()

        await asyncio.gather(watch_task, restart_task)
        click.clear()

    # Check if is Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        pass

    asyncio.run(main())
