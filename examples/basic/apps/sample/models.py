from zmag import m


@m.type
class User:
    name: m.use[str] = m.col(m.str, index=True)


User()
