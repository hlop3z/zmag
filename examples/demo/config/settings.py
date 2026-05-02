"""Project settings configuration."""

from pathlib import Path

# Base directory of the project
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Apps to load (always installed, regardless of mode)
INSTALLED_APPS: list = []

# Plugins for extending functionality
PLUGINS: dict = {}

# Database. Framework picks the async driver from ``engine`` — no need to
# remember aiosqlite/asyncpg. Sqlite paths are anchored at BASE_DIR if relative.
DATABASE: dict = {
    "engine": "sqlite",  # postgres | sqlite
    "sqlite": "db.sqlite3",
    # IMPORTANT: in production...
    # USE: os.getenv()
    "postgres": {
        "name": "db_name",
        "user": "db_user",
        "pass": "db_password",
        "host": "localhost",
        "port": "5432",
    },
}
