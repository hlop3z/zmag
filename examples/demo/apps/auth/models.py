from zmag import m

if m.typing:
    from apps.sample_app.models import Blog


@m.type(index=[("first_name", "last_name")], unique=[("first_name", "last_name")])
class User(m.Model):
    first_name: m.use[str] = m.col(m.str, cleanup=["strip", "lower"])
    last_name: m.use[str] = m.col(m.str)
    full_name: m.use[str] = m.col(m.str, computed="first_name || ' ' || last_name")
    blogs: m.refs["Blog"] = m.col("sample_app.Blog.id", m2m=True)

    class CRUD(m.CRUD):  # ...
        async def validor(self, ctx: m.Context, mode: str):
            match mode:
                case "create":
                    print(ctx.input)
                case "update":
                    print(ctx.input)

        async def get(self, ctx: m.Context):
            extra = [("created_at", "gt", "2026-05-02T08:41:28.543150")]
            """
            ctx.error(code="404", message="Error Message")
            if len(ctx.errors) > 0:
                return None
            """
            print("USER", ctx.user)
            return await self.orm.get(ctx.db, ctx.id, extra)

        async def list(self, ctx: m.Context):
            extra = [("created_at", "gt", "2026-05-02T08:41:28.543150")]
            return await self.orm.list(ctx.db, ctx.pagination, ctx.filters + extra)
