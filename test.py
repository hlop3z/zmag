import asyncio
import httpx

_AUTH_KEY = ""


def auth(key=None):
    return {"Authorization": f"Bearer {key or _AUTH_KEY}"}


async def register_login():
    global _AUTH_KEY
    base_url = "http://127.0.0.1:8000"

    # Create Account (separate client — register may close the connection on retry)
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        try:
            await client.get("/api/auth/register")
        except httpx.HTTPError:
            pass

    # Login (fresh connection)
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        res = await client.post(
            "/api/auth/token",
            headers={"accept": "application/json"},
            data={
                "grant_type": "password",
                "username": "john@doe.com",
                "password": "secret",
            },
        )
        if res.status_code == 200:
            _AUTH_KEY = res.json()["access_token"]
            print("Login:", res.json())
        else:
            print("Login failed:", res.status_code, res.text)


async def test_catch_all():
    # Login
    await register_login()

    # CRUD TEST
    async with httpx.AsyncClient(
        base_url="http://localhost:8000",
        headers={**auth()},
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
