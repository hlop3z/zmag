import zmag
from zmag import m


@m.type(index=[("first_name", "last_name")], unique=[("id", "last_name")])
class User(zmag.Model):
    first_name: m.use[str] = m.col(m.str)
    last_name: m.use[str] = m.col(m.str)
    full_name: m.use[str] = m.col(m.str, computed="first_name || ' ' || last_name")


@m.type
class Blog(zmag.FullModel):
    name: m.use[str] = m.col(m.str)
    user_id: m.use[str] = m.col("sample.User.id")
    users: m.use[str] = m.col("sample.User.id", m2m=True)


User()
Blog()
