server_process = None  # Global variable to hold the server process


def watcher(host, port):
    import os
    import asyncio
    import watchgod
    import multiprocessing

    from .debug_server import debug_server
    from .watcher_linter import watch_linter

    restart_event = asyncio.Event()

    async def watch_files():
        async for changes in watchgod.awatch(".", watcher_cls=watchgod.DefaultWatcher):
            restart_event.set()  # Set the event to signal a restart

    async def restart_server(host, port):
        global server_process

        while True:
            await restart_event.wait()  # Wait for the event to be set
            restart_event.clear()  # Clear the event flag

            print("Restarting Server...")

            if server_process:
                server_process.terminate()
                server_process.join()

            server_process = multiprocessing.Process(
                target=debug_server, args=(host, port)
            )
            server_process.start()

    async def main(host, port):
        watch_task = asyncio.create_task(watch_files())
        restart_task = asyncio.create_task(restart_server(host, port))
        linter_task = asyncio.create_task(watch_linter())

        restart_event.set()

        await asyncio.gather(watch_task, restart_task, linter_task)

    # Check if is Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        pass

    asyncio.run(main(host, port))
