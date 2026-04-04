# Mood Weather

> A visual mood tracking application using weather metaphors

## Overview

Mood Weather is a simple but complete mood tracking application that lets users log their daily mood using weather icons (sunny, cloudy, rainy, stormy). The project follows a modern full-stack architecture with a FastAPI backend, React frontend, and PostgreSQL database.

## Product Description

**End user:** People who want to track their daily mood in a simple, visual way.

**Problem:** Traditional mood trackers feel like chores — users have to rate themselves on scales or answer long questionnaires, so they stop using them.

**Product idea:** Users pick a weather icon each day (sunny, cloudy, rainy, stormy) to represent their mood, creating a personal "weather calendar" that's easy to understand at a glance.

**Core feature:** Daily mood selection with weather icons — one tap per day, displayed as a monthly calendar view where each day shows a weather icon instead of a number or text.

**Additional feature:** Mood trends — a simple bar chart showing how many sunny/cloudy/rainy days the user had over the past month.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│    Caddy    │────▶│   FastAPI   │
│  (React)    │◀────│   (Proxy)   │◀────│  (Backend)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │  PostgreSQL │
                                        └─────────────┘
```

## Quick Start

```bash
# Clone and start the application
docker compose up --build

# Access the application
# Frontend: http://localhost:42002
# API docs: http://localhost:42002/docs
```

## Project Structure

```
se-toolkit-mood-weather/
├── backend/              # FastAPI backend
│   ├── src/mood_weather/ # Application source
│   │   ├── main.py       # FastAPI app
│   │   ├── models/       # SQLModel models
│   │   ├── routers/      # API routers
│   │   ├── db/           # Database operations
│   │   └── data/         # SQL init scripts
│   └── tests/            # Unit and e2e tests
├── client-web-react/     # React frontend
│   └── src/
│       ├── App.tsx       # Main app component
│       └── Dashboard.tsx # Analytics dashboard
├── caddy/                # Caddy reverse proxy
├── mcp/                  # MCP server (for agent integration)
│   └── mcp-mood-weather/
├── docker-compose.yml    # Docker orchestration
└── docs/                 # Documentation
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/moods/` | List mood entries |
| POST | `/moods/` | Create mood entry |
| GET | `/moods/{id}` | Get mood entry |
| DELETE | `/moods/{id}` | Delete mood entry |
| GET | `/users/` | List users |
| POST | `/users/` | Create user |
| GET | `/analytics/summary` | Mood summary |
| GET | `/analytics/timeline` | Mood timeline |
| GET | `/analytics/streak` | Current streak |

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLModel, asyncpg
- **Frontend:** React 18, TypeScript, Vite, Chart.js
- **Database:** PostgreSQL 18
- **Proxy:** Caddy 2
- **Testing:** pytest, pytest-asyncio, httpx

## License

MIT
