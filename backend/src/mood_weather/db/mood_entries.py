"""Database operations for mood entries."""

from datetime import date
from typing import Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from mood_weather.models.mood_entry import MoodEntry, MoodEntryCreate


async def create_mood_entry(
    session: AsyncSession, entry_data: MoodEntryCreate
) -> MoodEntry:
    """Create a new mood entry."""
    entry = MoodEntry.model_validate(entry_data)
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def get_mood_entries_by_user(
    session: AsyncSession,
    user_id: str,
    limit: int = 100,
    offset: int = 0,
) -> list[MoodEntry]:
    """Get mood entries for a user, ordered by date descending."""
    stmt = (
        select(MoodEntry)
        .where(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.entry_date.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_mood_entries_by_date_range(
    session: AsyncSession,
    user_id: str,
    start_date: date,
    end_date: date,
) -> list[MoodEntry]:
    """Get mood entries for a user within a date range."""
    stmt = (
        select(MoodEntry)
        .where(MoodEntry.user_id == user_id)
        .where(MoodEntry.entry_date >= start_date)
        .where(MoodEntry.entry_date <= end_date)
        .order_by(MoodEntry.entry_date.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_mood_entry_by_user_and_date(
    session: AsyncSession,
    user_id: str,
    entry_date: date,
) -> Optional[MoodEntry]:
    """Get a single mood entry for a user on a specific date."""
    stmt = (
        select(MoodEntry)
        .where(MoodEntry.user_id == user_id)
        .where(MoodEntry.entry_date == entry_date)
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_mood_entry(
    session: AsyncSession,
    entry_id: int,
    weather_type: Optional[str] = None,
    note: Optional[str] = None,
) -> Optional[MoodEntry]:
    """Update an existing mood entry."""
    stmt = select(MoodEntry).where(MoodEntry.id == entry_id)
    result = await session.execute(stmt)
    entry = result.scalars().first()
    if not entry:
        return None

    if weather_type is not None:
        entry.weather_type = weather_type
    if note is not None:
        entry.note = note

    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry
