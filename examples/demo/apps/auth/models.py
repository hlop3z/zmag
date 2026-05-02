from zmag import m
from datetime import datetime

if m.typing:
    from apps.sample_app.models import Blog


@m.type(index=[("first_name", "last_name")], unique=[("first_name", "last_name")])
class User(m.Model):
    first_name: m.use[str] = m.col(m.str)
    last_name: m.use[str] = m.col(m.str)
    full_name: m.use[str] = m.col(m.str, computed="first_name || ' ' || last_name")
    blogs: m.refs["Blog"] = m.col("sample_app.Blog.id", m2m=True)

    class CRUD(m.CRUD):

        async def list(self, ctx: m.Context):
            return await self.orm.filter(ctx.db, ctx.filters)
