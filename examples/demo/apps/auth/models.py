from zmag import m

if m.typing:
    from apps.sample_app.models import Blog


@m.type
class User(m.Model):
    email: m.use[str] = m.col(m.str, unique=True)
    password: m.use[str] = m.col(m.str)
    disabled: m.use[bool] = m.col(m.bool, default=False)

    first_name: m.use[str] = m.col(m.str, cleanup=["strip", "lower"], nullable=True)
    last_name: m.use[str] = m.col(m.str, nullable=True)
    full_name: m.use[str] = m.col(
        m.str, computed="first_name || ' ' || last_name", nullable=True
    )

    class CRUD(m.CRUD): ...
