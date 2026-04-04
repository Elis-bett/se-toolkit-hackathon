"""HTTP client for the Mood Weather API."""

from typing import Optional
import httpx
from mcp_mood_weather.models import (
    HealthResult,
    MoodEntry,
    SummaryResult,
    StreakResult,
    TimelineEntry,
)
from mcp_mood_weather.settings import Settings


class MoodWeatherClient:
    """Async HTTP client for the Mood Weather API."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._client = httpx.AsyncClient(
            base_url=self.settings.base_url,
            headers={"Authorization": f"Bearer {self.settings.api_key}"},
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def health_check(self) -> HealthResult:
        """Check API health."""
        response = await self._client.get("/health")
        response.raise_for_status()
        return HealthResult(**response.json())

    async def get_mood_entries(
        self, user_id: str, limit: int = 100, offset: int = 0
    ) -> list[MoodEntry]:
        """Get mood entries for a user."""
        response = await self._client.get(
            "/moods/", params={"user_id": user_id, "limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return [MoodEntry(**entry) for entry in response.json()]

    async def create_mood_entry(
        self,
        user_id: str,
        entry_date: str,
        weather_type: str,
        note: Optional[str] = None,
    ) -> MoodEntry:
        """Create a mood entry."""
        payload = {
            "user_id": user_id,
            "entry_date": entry_date,
            "weather_type": weather_type,
        }
        if note:
            payload["note"] = note

        response = await self._client.post("/moods/", json=payload)
        response.raise_for_status()
        return MoodEntry(**response.json())

    async def get_summary(self, user_id: str, days: int = 30) -> SummaryResult:
        """Get mood summary."""
        response = await self._client.get(
            "/analytics/summary", params={"user_id": user_id, "days": days}
        )
        response.raise_for_status()
        return SummaryResult(**response.json())

    async def get_timeline(self, user_id: str, days: int = 30) -> list[TimelineEntry]:
        """Get mood timeline."""
        response = await self._client.get(
            "/analytics/timeline", params={"user_id": user_id, "days": days}
        )
        response.raise_for_status()
        return [TimelineEntry(**entry) for entry in response.json()]

    async def get_streak(self, user_id: str) -> StreakResult:
        """Get current streak."""
        response = await self._client.get(
            "/analytics/streak", params={"user_id": user_id}
        )
        response.raise_for_status()
        return StreakResult(**response.json())
