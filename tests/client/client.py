# -*- coding: utf-8 -*-
"""
ZMAG Client
"""

# Python
import asyncio
import multiprocessing
import os
import threading
import timeit
from types import SimpleNamespace

# Set Env for Client Mode
os.environ["ZMAG_TYPE"] = "1"

# ZMAG
import zmag

# import time
# from pathlib import Path

TIMEIT = False
IS_SYNC = True

MODE = "queue"
TEST_COUNT = 1
PORT = 5555

DEMO_PUBLICKEY = "2x.Y>2(J]I:$7i+CS<BVZMJyXEX)H8?31k5o)?mQ"
AUTHENTICATION = SimpleNamespace(
    publickey="1oQj?Q{i3#54qr)EZDx^:9O]jkCf9rfFWrhX(Ilg",
    secretkey="KQ}<GYmCZna=jmL8!REG1k)JMzJ7OTGu)j<*Xdp?",
    serverkey=DEMO_PUBLICKEY,
)


client = zmag.Frontend(
    is_sync=IS_SYNC,
    host=f"tcp://127.0.0.1:{PORT}",
    mode=MODE,
    # **AUTHENTICATION.__dict__,
    # base_dir=CURRENT_PATH,
    # fragments={"Author": "fragments/author.graphql"},
)


TEST_SIMPLE = """query MyQuery { demoBookList { id title } }"""
TEST_COMPLEX = """
query MyQuery {
  bookList(pagination: {page: 0}) {
    edges {
      cursor
      node {
        id
        titles
        author {
          fullName
        }
      }
    }
  }
}
"""

ARGS = SimpleNamespace(
    query=TEST_COMPLEX,
    variables={},
    operation="MyQuery",
    context={
        "user": {
            "id": 1,
            "username": "admin",
            "firstName": "",
            "lastName": "",
            "email": "admin@example.com",
            "isStaff": True,
            "isActive": True,
            "isSuperuser": True,
            "isAuthenticated": True,
            "lastLogin": "2024-08-10T21:19:39.082111+00:00",
            "dateJoined": "2024-08-02T17:21:11.081936+00:00",
        }
    },
)


def test_sync_subscribe():
    """Subscribe Sync"""
    while True:
        message = client.subscribe("")
        print("Received:", message)


def test_sync_pull():
    """Pull Sync"""
    while True:
        work = client.pull()
        print("Received:", work)


def test_sync_request():
    """Request Sync"""
    for _ in range(TEST_COUNT):
        response = client.request(**ARGS.__dict__)
        print(response.body)


def test_sync():
    """Tests Sync"""
    match MODE:
        case "forwarder":
            test_sync_subscribe()
        case "streamer":
            test_sync_pull()
        case _:
            test_sync_request()
    #
    # test_sync_pull()


async def test_async():
    """Test Async"""
    for _ in range(TEST_COUNT):
        response = await client.request(**ARGS.__dict__)
        print(response)


def thread_worker():
    """Function to create and manage 10 threads in each process."""
    threads = []
    for _ in range(500):
        thread = threading.Thread(target=test_sync)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to finish


def process_worker():
    processes = []
    for _ in range(10):
        process = multiprocessing.Process(target=thread_worker)
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()


def main():
    """Main"""
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if IS_SYNC:
        test_sync()
        if TIMEIT:
            timer = timeit.timeit(process_worker, number=1)
            print(timer)
    else:
        asyncio.run(test_async())


if __name__ == "__main__":
    main()
