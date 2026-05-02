import asyncio

import zmag

if zmag.typing:
    from apps.sample.models import Blog, User

from zmag.database.sql_sessions import async_session


async def main():
    # ── Bootstrap ────────────────────────────────────────────────────────────
    zmag.create_tables()

    User: User = zmag.get_model("sample", "User")
    Blog: Blog = zmag.get_model("sample", "Blog")

    async with async_session() as session:

        # ── CREATE ───────────────────────────────────────────────────────────
        user_id: str = (
            await session.execute(
                User.orm.create({"first_name": "John", "last_name": "Doe"})
            )
        ).scalar_one()

        blog_id: str = (
            await session.execute(
                Blog.orm.create({"name": "My Blog", "meta": {}, "user_id": user_id})
            )
        ).scalar_one()

        await session.commit()
        print("Created user:", user_id)
        print("Created blog:", blog_id)

        # ── READ ─────────────────────────────────────────────────────────────
        user_row = (await session.execute(User.orm.get(user_id))).mappings().first()
        print("User:", dict(user_row) if user_row else None)

        # ── FILTER ───────────────────────────────────────────────────────────
        stmt = Blog.orm.filter([("name", "like", "%Blog%")])
        blogs = (await session.execute(stmt)).mappings().all()
        print("Blogs matching 'Blog':", [dict(b) for b in blogs])

        # ── UPDATE ───────────────────────────────────────────────────────────
        await session.execute(Blog.orm.update(blog_id, {"name": "Updated Blog"}))
        await session.commit()
        print("Updated blog name")

        # ── M2M: link ────────────────────────────────────────────────────────
        await session.execute(Blog.m2m.users(blog_id).add(user_id))
        await session.commit()
        print("Linked user to blog")

        # ── M2M: query through junction ───────────────────────────────────────
        stmt = Blog.m2m.users(blog_id).of()
        users = (await session.execute(stmt)).mappings().all()
        print("Users on blog:", [dict(u) for u in users])

        # chain extra filters on top
        stmt = Blog.m2m.users(blog_id).of().where(User.orm.table.c.first_name == "John")
        users_named_john = (await session.execute(stmt)).mappings().all()
        print("Users named John on blog:", [dict(u) for u in users_named_john])

        # ── M2M: unlink ───────────────────────────────────────────────────────
        await session.execute(Blog.m2m.users(blog_id).remove(user_id))
        await session.commit()
        print("Unlinked user from blog")

        # ── DELETE ────────────────────────────────────────────────────────────
        # await session.execute(Blog.orm.delete(blog_id))
        # await session.execute(User.orm.delete(user_id))
        await session.commit()
        print("Deleted blog and user")


if __name__ == "__main__":
    asyncio.run(main())
