from datetime import datetime, timezone

from jinja2 import Template


def utc_now():
    return datetime.now(timezone.utc)


def load_template(path: str) -> Template:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Template(content)
