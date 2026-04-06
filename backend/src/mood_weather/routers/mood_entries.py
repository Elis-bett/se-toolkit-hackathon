"""Mood entries router with CRUD endpoints."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from mood_weather.database import get_session
from mood_weather.models.mood_entry import MoodEntry, MoodEntryCreate, MoodEntryRead, MoodEntryUpdate
from mood_weather.db.mood_entries import (
    create_mood_entry,
    get_mood_entries_by_user,
    get_mood_entry_by_user_and_date,
    update_mood_entry,
)

router = APIRouter(prefix="/moods", tags=["moods"])


@router.get("/", response_model=list[MoodEntryRead])
async def list_mood_entries(
    user_id: str = Query(..., description="Filter by user ID"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> list[MoodEntryRead]:
    """List mood entries for a user."""
    entries = await get_mood_entries_by_user(
        session, user_id=user_id, limit=limit, offset=offset
    )
    return entries


@router.get("/{entry_id}", response_model=MoodEntryRead)
async def get_mood_entry(
    entry_id: int,
    session: AsyncSession = Depends(get_session),
) -> MoodEntryRead:
    """Get a specific mood entry by ID."""
    stmt = select(MoodEntry).where(MoodEntry.id == entry_id)
    result = await session.execute(stmt)
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return entry


@router.post("/", response_model=MoodEntryRead, status_code=status.HTTP_201_CREATED)
async def create_mood_entry_endpoint(
    entry_data: MoodEntryCreate,
    session: AsyncSession = Depends(get_session),
) -> MoodEntryRead:
    """Create a new mood entry."""
    # Check if entry already exists for this user on this date
    existing = await get_mood_entry_by_user_and_date(
        session, user_id=entry_data.user_id, entry_date=entry_data.entry_date
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Mood entry already exists for this user on this date",
        )

    entry = await create_mood_entry(session, entry_data)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood_entry(
    entry_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a mood entry."""
    stmt = select(MoodEntry).where(MoodEntry.id == entry_id)
    result = await session.execute(stmt)
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")

    await session.delete(entry)
    await session.commit()


@router.put("/{entry_id}", response_model=MoodEntryRead)
async def update_mood_entry_endpoint(
    entry_id: int,
    update_data: MoodEntryUpdate,
    session: AsyncSession = Depends(get_session),
) -> MoodEntryRead:
    """Update an existing mood entry."""
    entry = await update_mood_entry(
        session,
        entry_id=entry_id,
        weather_type=update_data.weather_type,
        note=update_data.note,
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return entry
