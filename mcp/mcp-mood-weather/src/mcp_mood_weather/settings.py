"""Settings for the MCP server."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the MCP Mood Weather client."""

    base_url: str = "http://localhost:42001"
    api_key: str = "dev-secret-key"

    model_config = {
        "env_prefix": "MOOD_WEATHER_MCP_",
    }


def resolve_settings() -> Settings:
    """Resolve settings from environment variables or defaults."""
    # Also check NANOBOT_* prefix for compatibility
    base_url = os.getenv("MOOD_WEATHER_MCP_BASE_URL") or os.getenv(
        "NANOBOT_MOOD_WEATHER_URL", "http://localhost:42001"
    )
    api_key = os.getenv("MOOD_WEATHER_MCP_API_KEY") or os.getenv(
        "NANOBOT_MOOD_WEATHER_API_KEY", "dev-secret-key"
    )

    return Settings(base_url=base_url, api_key=api_key)
