"""E2E tests for mood entries endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_moods_returns_200(client: AsyncClient):
    """Test that GET /moods/ returns 200."""
    response = await client.get("/moods/", params={"user_id": "e2e-test-user"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_moods_returns_list(client: AsyncClient):
    """Test that GET /moods/ returns a list."""
    response = await client.get("/moods/", params={"user_id": "e2e-test-user"})
    data = response.json()
    assert isinstance(data, list)
