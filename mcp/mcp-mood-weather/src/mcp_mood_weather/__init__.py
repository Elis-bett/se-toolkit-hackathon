"""MCP Mood Weather server package."""

from mcp_mood_weather.server import create_server, main
from mcp_mood_weather.client import MoodWeatherClient
from mcp_mood_weather.models import HealthResult, MoodEntry, SummaryResult, StreakResult
from mcp_mood_weather.settings import Settings

__all__ = [
    "create_server",
    "main",
    "MoodWeatherClient",
    "HealthResult",
    "MoodEntry",
    "SummaryResult",
    "StreakResult",
    "Settings",
]
