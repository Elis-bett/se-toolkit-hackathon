"""Application settings loaded from environment variables."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the Mood Weather application."""

    api_key: str = "dev-secret-key"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "moodweather"
    db_user: str = "mooduser"
    db_password: str = "moodpass"
    use_sqlite: bool = False

    model_config = {
        "env_prefix": "MOOD_WEATHER_",
    }

    @property
    def database_url(self) -> str:
        """Build async SQLAlchemy database URL."""
        if self.use_sqlite:
            return "sqlite+aiosqlite:///./moodweather.db"
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_database_url(self) -> str:
        """Build sync SQLAlchemy database URL (for tests with SQLite)."""
        return "sqlite+aiosqlite:///:memory:"


settings = Settings()
