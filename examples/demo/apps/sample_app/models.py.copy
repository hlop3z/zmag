from zmag import m

if m.typing:
    from apps.auth.models import User


@m.type
class Blog(m.FullModel):
    name: m.use[str] = m.col(m.str)
    tags: m.use[m.List] = m.col(m.json)
    meta: m.use[m.Dict] = m.col(m.json)
    owner_id: m.use[int] = m.col("auth.User.id")
    owner: m.use["User"] = None
    authors: m.refs["User"] = m.col("auth.User.id", m2m=True)
