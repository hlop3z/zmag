from config import settings

BASE_DIR = getattr(settings, "BASE_DIR")
DATABASE = getattr(settings, "DATABASE", {})
DB_ENGINE = DATABASE.get("engine")


def get_databe_url() -> str:
    match DB_ENGINE:
        case "sqlite":
            name = DATABASE.get("sqlite")
            return f"sqlite+aiosqlite:///{ BASE_DIR / name }"
        case "postgres":
            conf = DATABASE.get("postgres", {})
            name = f"{conf.get("USER")}:{conf.get("PASS")}@{conf.get("HOST")}:{conf.get("PORT")}/{conf.get("NAME")}"
            return f"postgresql+asyncpg://{name}"
        case _:
            return f"sqlite+aiosqlite:///{ BASE_DIR / "db.sqlite3" }"


DB_URL = get_databe_url()
