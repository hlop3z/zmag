import asyncio
import httpx


def auth(key):
    return {"Authorization": f"Bearer {key}"}


async def test_catch_all():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000",
        headers={
            **auth(
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huQGRvZS5jb20iLCJleHAiOjE3Nzc3OTY3NjEsInR5cGUiOiJhY2Nlc3MifQ.8WWC3YZ5zSAbauQJdy1NIkiaBKH3jug923_2Mavb0mU"
            )
        },
    ) as client:
        app_name = "sample-app"
        model_name = "blog"

        res = await client.post(
            f"/api/crud/{app_name}/{model_name}",
            json={"name": "my-post"},
        )
        if res.status_code == 200:
            print("CREATE:", res.json())

        item_id = (res.json().get("data") or {}).get("id")

        if item_id:
            res = await client.get(f"/api/crud/{app_name}/{model_name}?id={item_id}")
            if res.status_code == 200:
                print("GET   :", res.json())

            res = await client.patch(
                f"/api/crud/{app_name}/{model_name}",
                json={"name": "new-name"},
            )
            if res.status_code == 200:
                print("UPDATE:", res.json())

            res = await client.patch(
                f"/api/crud/{app_name}/{model_name}?id={item_id}",
                json={"name": []},
            )
            if res.status_code == 200:
                print("UPDATE :", res.json())

            res = await client.get(f"/api/crud/{app_name}/{model_name}")
            if res.status_code == 200:
                print("LIST  :", res.json())

            """
            res = await client.delete(f"/api/crud/{app_name}/{model_name}?id={item_id}")
            if res.status_code == 200:
                print("DELETE:", res.json())
            """


if __name__ == "__main__":
    asyncio.run(test_catch_all())
