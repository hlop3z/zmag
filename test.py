import asyncio
import httpx


async def test_catch_all():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        app_name = "auth"
        model_name = "user"

        res = await client.post(
            f"/api/public/{app_name}/{model_name}",
            json={"first_name": "john", "last_name": "doe"},
        )
        print("CREATE:", res.json())

        user_id = (res.json().get("data") or {}).get("id")

        if user_id:
            res = await client.get(f"/api/public/{app_name}/{model_name}?id={user_id}")
            print("GET   :", res.json())

            res = await client.put(
                f"/api/public/{app_name}/{model_name}?id={user_id}",
                json={"first_name": "jane"},
            )
            print("UPDATE:", res.json())

            res = await client.patch(
                f"/api/public/{app_name}/{model_name}?id={user_id}",
                json={"last_name": "smith"},
            )
            print("PATCH :", res.json())

            res = await client.get(
                f"/api/public/{app_name}/{model_name}?first_name__eq=jane"
            )
            print("LIST  :", res.json())

            res = await client.delete(
                f"/api/public/{app_name}/{model_name}?id={user_id}"
            )
            print("DELETE:", res.json())


if __name__ == "__main__":
    asyncio.run(test_catch_all())
