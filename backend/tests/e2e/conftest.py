"""Pytest configuration for e2e tests."""

import os
import pytest
from httpx import AsyncClient

GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://localhost:42002")
API_KEY = os.getenv("MOOD_WEATHER_API_KEY", "dev-secret-key")


@pytest.fixture
async def client():
    """Create an async test client pointing to the running server."""
    async with AsyncClient(base_url=GATEWAY_BASE_URL) as ac:
        yield ac
