# Python
import asyncio
import os
import time
from pathlib import Path

# ZMAG
from zmag import Frontend

IS_SYNC = True

TEST_COUNT = 2
PORT = 5555

MODE = "forwarder"
DEMO_PUBLICKEY = "2x.Y>2(J]I:$7i+CS<BVZMJyXEX)H8?31k5o)?mQ"


client = Frontend(
    is_sync=IS_SYNC,
    host=f"tcp://127.0.0.1:{PORT}",
    mode=MODE,
    # base_dir=CURRENT_PATH,
    # fragments={"Author": "fragments/author.graphql"},
    publickey="1oQj?Q{i3#54qr)EZDx^:9O]jkCf9rfFWrhX(Ilg",
    secretkey="KQ}<GYmCZna=jmL8!REG1k)JMzJ7OTGu)j<*Xdp?",
    serverkey=DEMO_PUBLICKEY,
)


TEST_SIMPLE = """query MyQuery { demoBookList { id title } }"""
TEST_COMPLEX = """
query MyQuery {
  demoBookList {
    id
    title
    author {
      id
      name
    }
  }
}
"""

ARGS = dict(
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
    while True:
        message = client.subscribe("")
        print("Received:", message)


def test_sync_pull():
    while True:
        work = client.pull()
        print("Received:", work)


def test_sync_request():
    for i in range(TEST_COUNT):
        response = client.request(**ARGS)
        print(response)


def test_sync():
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
    for i in range(TEST_COUNT):
        response = await client.request(**ARGS)
        print(response)


def main():
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if IS_SYNC:
        test_sync()
    else:
        asyncio.run(test_async())


if __name__ == "__main__":
    main()
