"""Tests for analytics endpoints."""

import pytest
from datetime import date, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_mood_summary(client: AsyncClient, db_session):
    """Test mood summary endpoint."""
    # Create some entries
    today = date.today()
    for i in range(5):
        await client.post(
            "/moods/",
            json={
                "user_id": "analytics-user-1",
                "entry_date": str(today - timedelta(days=i)),
                "weather_type": "sunny",
            },
        )

    for i in range(3):
        await client.post(
            "/moods/",
            json={
                "user_id": "analytics-user-1",
                "entry_date": str(today - timedelta(days=i + 5)),
                "weather_type": "cloudy",
            },
        )

    response = await client.get(
        "/analytics/summary", params={"user_id": "analytics-user-1", "days": 30}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "analytics-user-1"
    assert data["total_entries"] == 8
    assert data["distribution"]["sunny"] == 5
    assert data["distribution"]["cloudy"] == 3


@pytest.mark.asyncio
async def test_mood_timeline(client: AsyncClient, db_session):
    """Test mood timeline endpoint."""
    today = date.today()
    await client.post(
        "/moods/",
        json={
            "user_id": "analytics-user-2",
            "entry_date": str(today - timedelta(days=1)),
            "weather_type": "rainy",
        },
    )
    await client.post(
        "/moods/",
        json={
            "user_id": "analytics-user-2",
            "entry_date": str(today),
            "weather_type": "sunny",
        },
    )

    response = await client.get(
        "/analytics/timeline", params={"user_id": "analytics-user-2", "days": 7}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Should be ordered by date ascending
    assert data[0]["weather_type"] == "rainy"
    assert data[1]["weather_type"] == "sunny"


@pytest.mark.asyncio
async def test_current_streak(client: AsyncClient, db_session):
    """Test current streak endpoint."""
    today = date.today()
    # Create 3 consecutive days including today
    for i in range(3):
        await client.post(
            "/moods/",
            json={
                "user_id": "analytics-user-3",
                "entry_date": str(today - timedelta(days=i)),
                "weather_type": "sunny",
            },
        )

    response = await client.get(
        "/analytics/streak", params={"user_id": "analytics-user-3"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] == 3


@pytest.mark.asyncio
async def test_current_streak_no_entries(client: AsyncClient, db_session):
    """Test streak with no entries."""
    response = await client.get(
        "/analytics/streak", params={"user_id": "no-entries-user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] == 0
