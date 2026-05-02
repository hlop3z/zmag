from zmag import m

if m.typing:
    from apps.sample_app.models import Blog


@m.type(index=[("first_name", "last_name")], unique=[("first_name", "last_name")])
class User(m.Model):
    first_name: m.use[str] = m.col(m.str)
    last_name: m.use[str] = m.col(m.str)
    full_name: m.use[str] = m.col(m.str, computed="first_name || ' ' || last_name")
    blogs: m.refs["Blog"] = m.col("sample_app.Blog.id", m2m=True)

    class CRUD(m.Crud):
        async def create(self, ctx):
            stmt = self.orm.create(ctx.input)
            result = (await ctx.db.execute(stmt)).mappings().first()
            await ctx.db.commit()
            return result

        async def update(self, ctx):
            stmt = self.orm.update(ctx.id, ctx.input)
            await ctx.db.execute(stmt)
            await ctx.db.commit()
            return (await ctx.db.execute(self.orm.get(ctx.id))).mappings().first()

        async def patch(self, ctx):
            stmt = self.orm.update(ctx.id, ctx.input)
            await ctx.db.execute(stmt)
            await ctx.db.commit()
            return (await ctx.db.execute(self.orm.get(ctx.id))).mappings().first()

        async def delete(self, ctx):
            await ctx.db.execute(self.orm.delete(ctx.id))
            await ctx.db.commit()

        async def list(self, ctx):
            stmt = self.orm.filter(ctx.filters + [("last_name", "eq", "doe")])
            return (await ctx.db.execute(stmt)).mappings().all()

        async def get(self, ctx):
            stmt = self.orm.get(ctx.id)
            return (await ctx.db.execute(stmt)).mappings().first()
