import asyncio
import httpx


def auth(key):
    return {"Authorization": f"Bearer {key}"}


async def test_catch_all():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000",
        headers={
            **auth(
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzc3NzgzOTA3LCJ0eXBlIjoiYWNjZXNzIn0.CL5pH8AZO-tWFI20P378Ok_9-7f2VfHY0zA-n1EeObY"
            )
        },
    ) as client:
        app_name = "auth"
        model_name = "user"

        res = await client.post(
            f"/api/crud/{app_name}/{model_name}",
            json={"first_name": "john", "last_name": "doe"},
        )
        if res.status_code == 200:
            print("CREATE:", res.json())

        user_id = (res.json().get("data") or {}).get("id")

        if user_id:
            res = await client.get(f"/api/crud/{app_name}/{model_name}?id={user_id}")
            if res.status_code == 200:
                print("GET   :", res.json())

            res = await client.patch(
                f"/api/crud/{app_name}/{model_name}",
                json={"first_name": "jane"},
            )
            if res.status_code == 200:
                print("UPDATE:", res.json())

            res = await client.patch(
                f"/api/crud/{app_name}/{model_name}?id={user_id}",
                json={"first_name": "jane", "last_name": []},
            )
            if res.status_code == 200:
                print("UPDATE :", res.json())

            res = await client.get(f"/api/crud/{app_name}/{model_name}")
            if res.status_code == 200:
                print("LIST  :", res.json())

            res = await client.delete(f"/api/crud/{app_name}/{model_name}?id={user_id}")
            if res.status_code == 200:
                print("DELETE:", res.json())


if __name__ == "__main__":
    asyncio.run(test_catch_all())
