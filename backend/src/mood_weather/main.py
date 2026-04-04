"""FastAPI application factory and main app setup."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from mood_weather.database import init_db
from mood_weather.routers.mood_entries import router as mood_entries_router
from mood_weather.routers.users import router as users_router
from mood_weather.routers.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title="Mood Weather API",
    description="A visual mood tracking API using weather metaphors",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


# Register routers
app.include_router(mood_entries_router)
app.include_router(users_router)
app.include_router(analytics_router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}
