from functools import lru_cache
from pathlib import Path

import pydantic as pd
from dotenv import load_dotenv

from file_uploader.logging import get_logger

logger = get_logger(__name__)

load_dotenv()


def validate_env_var(varname, v):
    if not v:
        raise ValueError(f"`{varname}` variable is empty")
    return v


class Settings(pd.BaseSettings):
    MEDIA_DIR: Path = Path('/media_content')
    MEDIA_POSTGRES_DB: str
    MEDIA_POSTGRES_HOST: str
    MEDIA_POSTGRES_HOST_FOR_ALEMBIC: str
    MEDIA_POSTGRES_USER: str
    MEDIA_POSTGRES_PORT: int
    MEDIA_POSTGRES_PASSWORD: str
    MEDIA_DB_CONNECT_RETRY: int
    MEDIA_DB_POOL_SIZE: int
    SCHEDULE_SERVICE_HOSTS: str

    class Config:
        env_file = '.env'

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.MEDIA_POSTGRES_DB,
            "user": self.MEDIA_POSTGRES_USER,
            "password": self.MEDIA_POSTGRES_PASSWORD,
            "host": self.MEDIA_POSTGRES_HOST,
            "host_for_alembic": self.MEDIA_POSTGRES_HOST_FOR_ALEMBIC,
            "port": self.MEDIA_POSTGRES_PORT,
        }

    def get_sync_database_uri_alembic(self):
        return "postgresql://{user}:{password}@{host_for_alembic}:{port}/{database}".format(
            **self.database_settings,
        )

    def get_sync_database_uri(self):
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    def get_async_database_uri(self):
        logger.debug("Use asyncpg driver for db access")
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


SETTINGS: Settings = get_settings()
