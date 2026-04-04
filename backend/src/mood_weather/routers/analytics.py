"""Analytics router for mood statistics and trends."""

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func, col

from mood_weather.database import get_session
from mood_weather.models.mood_entry import MoodEntry

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
async def get_mood_summary(
    user_id: str = Query(..., description="Filter by user ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Get a summary of mood distribution over the past N days."""
    start_date = date.today() - timedelta(days=days)

    stmt = (
        select(MoodEntry.weather_type, func.count(MoodEntry.id).label("count"))
        .where(MoodEntry.user_id == user_id)
        .where(MoodEntry.entry_date >= start_date)
        .group_by(MoodEntry.weather_type)
    )
    result = await session.execute(stmt)

    distribution = {}
    total = 0
    for weather_type, count in result.all():
        distribution[weather_type] = count
        total += count

    return {
        "user_id": user_id,
        "days": days,
        "total_entries": total,
        "distribution": distribution,
    }


@router.get("/timeline")
async def get_mood_timeline(
    user_id: str = Query(..., description="Filter by user ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """Get daily mood entries for timeline visualization."""
    start_date = date.today() - timedelta(days=days)

    stmt = (
        select(MoodEntry.entry_date, MoodEntry.weather_type)
        .where(MoodEntry.user_id == user_id)
        .where(MoodEntry.entry_date >= start_date)
        .order_by(MoodEntry.entry_date.asc())
    )
    result = await session.execute(stmt)

    return [
        {"date": str(entry_date), "weather_type": weather_type}
        for entry_date, weather_type in result.all()
    ]


@router.get("/streak")
async def get_current_streak(
    user_id: str = Query(..., description="Filter by user ID"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Get the current streak of consecutive days with mood entries."""
    stmt = (
        select(MoodEntry.entry_date)
        .where(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.entry_date.desc())
    )
    result = await session.execute(stmt)
    dates = [row for row in result.scalars().all()]

    if not dates:
        return {"user_id": user_id, "current_streak": 0}

    current_streak = 1
    today = date.today()

    # Check if there's an entry today or yesterday (streak is still active)
    if dates[0] < today - timedelta(days=1):
        return {"user_id": user_id, "current_streak": 0}

    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            current_streak += 1
        else:
            break

    return {"user_id": user_id, "current_streak": current_streak}
