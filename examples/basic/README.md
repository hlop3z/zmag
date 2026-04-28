# basic

A zmag project.

## Quick start

```bash
uv sync
uv run python main.py db init
uv run python main.py start-app --name blogs
uv run python main.py db sync --message "initial"
uv run python main.py run --reload
```
