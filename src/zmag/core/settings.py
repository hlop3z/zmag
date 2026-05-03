from spoc import SingletonMeta

from config import settings as project_settings


def require_attr(name, message=None):
    obj = project_settings
    if not hasattr(obj, name):
        raise AttributeError(
            message or f"Missing required attribute in config/settings.py: {name}"
        )
    return getattr(obj, name)


class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self.base_dir = require_attr("BASE_DIR")
        # Database
        database = require_attr("DATABASE")
        self.databases = database
        self.db_engine = database.get("engine")
        self.db_url = self.__create_url()

    def __create_url(self):
        if self.db_engine == "sqlite":
            return f"sqlite+aiosqlite:///{self.base_dir / self.databases.get("sqlite")}"
        elif self.db_engine == "postgres":
            cfg = self.databases.get("postgres")
            return f"postgresql+asyncpg://{cfg.get("user")}:{cfg.get("pass")}@{cfg.get("host")}:{cfg.get("port")}/{cfg.get("name")}"


settings: Settings = Settings()
