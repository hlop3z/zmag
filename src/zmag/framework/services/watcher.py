# -*- coding: utf-8 -*-
"""
{ Watcher }
"""

import asyncio
import logging
import os
import signal
import sys
import time
from typing import Any

import click


# from .queue import start_queue
def start_watcher(spoc_worker, path_to_watch, banner, services):
    """Watch For File Changes"""

    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    banner_sleep_time = 1
    restart_event = asyncio.Event()

    def stop_loop_server():
        """Function to stop the event loop gracefully"""
        loop = asyncio.get_event_loop()
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()

    def server_stop_handler(sig, frame):  # pylint: disable=unused-argument
        """Signal handler to stop the server and loop"""
        logging.info("Shutting Down. . .")
        stop_loop_server()
        spoc_worker.stop(force_stop=True)
        # Exit
        sys.exit(0)
        # Force exit the main thread
        # os._exit(1)

    def listen_stop_server():
        """Function to set up signal handler for stopping the server"""
        signal.signal(signal.SIGINT, server_stop_handler)

    async def watch_directory(path_to_watch, on_modified):
        observer = Observer()
        event_handler: Any = FileSystemEventHandler()
        event_handler.on_modified = on_modified
        observer.schedule(event_handler, path=path_to_watch, recursive=True)
        observer.start()
        try:
            while True:
                await asyncio.sleep(1)  # Add a short sleep to avoid a busy loop
        finally:
            observer.stop()
            observer.join()

    def on_file_change(event):  # pylint: disable=unused-argument
        """File Changed"""
        restart_event.set()  # Signal to restart the service

    async def restart_server():
        """Restart Server"""

        while True:
            await restart_event.wait()  # Wait for the event to be set
            restart_event.clear()  # Clear the event flag

            spoc_worker.stop(timeout=0, forced_delay=0)
            spoc_worker.workers.clear()
            spoc_worker.add(*[s() for s in services])
            spoc_worker.start(False)
            click.clear()
            await asyncio.sleep(banner_sleep_time)
            time.sleep(banner_sleep_time)
            click.clear()
            banner()

    async def main():
        """Run Server"""
        watch_task = asyncio.create_task(watch_directory(path_to_watch, on_file_change))
        restart_task = asyncio.create_task(restart_server())
        restart_event.set()
        await asyncio.gather(watch_task, restart_task)
        click.clear()

    # Check if is Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Register signal handler
    listen_stop_server()

    # Run the main function
    asyncio.run(main())
