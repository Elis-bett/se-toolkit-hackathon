"""MoodEntry model for storing daily mood entries."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class MoodEntryBase(SQLModel):
    """Shared fields for mood entries."""

    user_id: str = Field(index=True)
    entry_date: date = Field(index=True)
    weather_type: str = Field(
        description=(
            "Weather icon representing the mood: "
            "sunny, partly_cloudy, cloudy, foggy, rainy, snowy, windy, hail, "
            "rainbow, hot, freezing, stormy, tornado"
        )
    )
    note: Optional[str] = Field(default=None, max_length=500)


class MoodEntry(MoodEntryBase, table=True):
    """Mood entry table model."""

    __tablename__ = "mood_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MoodEntryCreate(MoodEntryBase):
    """Schema for creating a mood entry."""


class MoodEntryRead(MoodEntryBase):
    """Schema for reading a mood entry."""

    id: int
    created_at: datetime


class MoodEntryUpdate(SQLModel):
    """Schema for updating a mood entry."""

    weather_type: Optional[str] = Field(
        default=None,
        description=(
            "Weather icon representing the mood: "
            "sunny, partly_cloudy, cloudy, foggy, rainy, snowy, windy, hail, "
            "rainbow, hot, freezing, stormy, tornado"
        )
    )
    note: Optional[str] = Field(default=None, max_length=500)
