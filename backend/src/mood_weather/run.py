"""Entry point for running the FastAPI application."""

import uvicorn

from mood_weather.main import app
from mood_weather.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "mood_weather.main:app",
        host="0.0.0.0",
        port=42001,
        reload=True,
    )
