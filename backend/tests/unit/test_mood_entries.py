"""Tests for mood entry endpoints."""

import pytest
from datetime import date
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_mood_entry(client: AsyncClient, db_session):
    """Test creating a mood entry."""
    response = await client.post(
        "/moods/",
        json={
            "user_id": "test-user-1",
            "entry_date": "2025-04-01",
            "weather_type": "sunny",
            "note": "Feeling great!",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "test-user-1"
    assert data["weather_type"] == "sunny"
    assert data["entry_date"] == "2025-04-01"


@pytest.mark.asyncio
async def test_create_duplicate_mood_entry(client: AsyncClient, db_session):
    """Test that creating a duplicate entry for same user/date fails."""
    entry_data = {
        "user_id": "test-user-2",
        "entry_date": "2025-04-01",
        "weather_type": "cloudy",
    }

    response1 = await client.post("/moods/", json=entry_data)
    assert response1.status_code == 201

    response2 = await client.post("/moods/", json=entry_data)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_list_mood_entries(client: AsyncClient, db_session):
    """Test listing mood entries for a user."""
    # Create entries
    await client.post(
        "/moods/",
        json={
            "user_id": "test-user-3",
            "entry_date": "2025-04-01",
            "weather_type": "sunny",
        },
    )
    await client.post(
        "/moods/",
        json={
            "user_id": "test-user-3",
            "entry_date": "2025-03-31",
            "weather_type": "cloudy",
        },
    )

    response = await client.get("/moods/", params={"user_id": "test-user-3"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Should be ordered by date descending
    assert data[0]["entry_date"] == "2025-04-01"
    assert data[1]["entry_date"] == "2025-03-31"


@pytest.mark.asyncio
async def test_list_mood_entries_empty(client: AsyncClient, db_session):
    """Test listing mood entries for a user with no entries."""
    response = await client.get("/moods/", params={"user_id": "nonexistent"})
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_delete_mood_entry(client: AsyncClient, db_session):
    """Test deleting a mood entry."""
    create_response = await client.post(
        "/moods/",
        json={
            "user_id": "test-user-4",
            "entry_date": "2025-04-01",
            "weather_type": "rainy",
        },
    )
    entry_id = create_response.json()["id"]

    delete_response = await client.delete(f"/moods/{entry_id}")
    assert delete_response.status_code == 204

    # Verify it's deleted
    get_response = await client.get(f"/moods/{entry_id}")
    assert get_response.status_code == 404
