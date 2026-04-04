"""Pydantic models for MCP responses."""

from pydantic import BaseModel
from typing import Optional


class HealthResult(BaseModel):
    """Health check result."""

    status: str
    version: str


class MoodEntry(BaseModel):
    """A mood entry."""

    id: int
    user_id: str
    entry_date: str
    weather_type: str
    note: Optional[str] = None


class SummaryResult(BaseModel):
    """Mood summary result."""

    user_id: str
    days: int
    total_entries: int
    distribution: dict[str, int]


class StreakResult(BaseModel):
    """Streak result."""

    user_id: str
    current_streak: int


class TimelineEntry(BaseModel):
    """Timeline entry."""

    date: str
    weather_type: str
