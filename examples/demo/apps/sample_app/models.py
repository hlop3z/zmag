from zmag import m

if m.typing:
    from apps.auth.models import User


@m.type
class Blog(m.FullModel):
    name: m.use[str] = m.col(m.str)
    owner_id: m.use[int] = m.col("auth.User.id", nullable=True)

    class CRUD(m.CRUD):
        async def validor(self, ctx: m.Context, mode: str):
            match mode:
                case "create":
                    print(ctx.input)
                case "update":
                    print(ctx.input)

        async def create(self, ctx: m.Context):
            if ctx.user:
                blog = Blog(name=ctx.input.get("name"), owner_id=ctx.user.id)
                return await self.orm.create(ctx.db, blog.__dict__)
            return None

        async def get(self, ctx: m.Context):
            extra = [("created_at", "gt", "2026-05-02T08:41:28.543150")]
            """
            ctx.error(code="404", message="Error Message")
            if len(ctx.errors) > 0:
                return None
            """
            return await self.orm.get(ctx.db, ctx.id, extra)

        async def list(self, ctx: m.Context):
            extra = [("created_at", "gt", "2026-05-02T08:41:28.543150")]
            return await self.orm.list(ctx.db, ctx.pagination, ctx.filters + extra)
