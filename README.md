# Mood Weather

> A visual mood tracking application using weather metaphors — one tap per day.

---

## Demo

> **Replace the screenshots below with actual images of your running application.**
> To capture them, run the app and take screenshots of:
> 1. The login screen
> 2. The mood tracker with calendar and entries

### Screenshot 1 — Login & Mood Selection
![Login Screen](docs/images/login-screen.png)

### Screenshot 2 — Calendar & Analytics Dashboard
![Dashboard](docs/images/dashboard.png)

---

## Product Context

### End Users
People who want to track their daily mood in a **simple, visual way** — no scales, no questionnaires, no friction.

### Problem
Traditional mood trackers feel like chores. Users have to rate themselves on numeric scales or answer long questionnaires, so they quickly stop using them.

### Our Solution
Mood Weather lets users pick **one of 13 weather icons** each day (sunny ☀️, cloudy ☁️, rainy 🌧️, stormy ⛈️, etc.) to represent their mood. This creates a personal **"weather calendar"** that's easy to understand at a glance and fun to use.

---

## Features

### ✅ Implemented

| Feature | Description |
|---------|-------------|
| **Mood Entry Creation** | Select a weather icon + optional note for any date |
| **Mood Entry Listing** | View recent entries with date, weather, and note |
| **Edit Mood Entries** | Update weather type and note inline (PUT `/moods/{id}`) |
| **Delete Mood Entries** | Remove entries with confirmation (DELETE `/moods/{id}`) |
| **Monthly Calendar View** | Visual calendar with weather icons for each day |
| **Analytics Dashboard** | Bar chart of mood distribution over time |
| **Mood Summary** | API endpoint for mood distribution (past N days) |
| **Mood Timeline** | Ordered list of entries (oldest first) |
| **Streak Tracking** | Current consecutive-day streak |
| **User Management** | Create and list users via API |
| **API Health Check** | `GET /health` — returns status and version |
| **Docker Compose Setup** | Full local development with one command |
| **VM Deployment** | Production-ready deployment on Ubuntu 24.04 |

### ❌ Not Yet Implemented

| Feature | Description |
|---------|-------------|
| **CSV Export** | Download mood data as CSV file |
| **Mood Insights** | Smart insights (e.g., "You tend to be sunny on weekends") |
| **Authentication** | Per-user login/password (currently uses API key) |
| **Push Notifications** | Daily reminders to log mood |
| **Dark Mode** | Toggle dark/light theme |

---

## Usage

### Quick Start (Local Development)

```bash
# 1. Clone the repository
git clone <repo-url>
cd se-toolkit-mood-weather

# 2. Start all services
docker compose up --build

# 3. Access the application
# Frontend:  http://localhost:42002
# API docs:  http://localhost:42002/docs
# Backend:   http://localhost:42001
```

### Logging In

On the frontend login screen, enter:

| Field | Value |
|-------|-------|
| **User ID** | Any string (e.g., `user1`) |
| **API Key** | `dev-secret-key` (or your configured `MOOD_WEATHER_API_KEY`) |

### Using the App

1. **Select a date** (defaults to today)
2. **Pick a weather icon** that matches your mood
3. **Add an optional note** (up to 500 characters)
4. **Click "Save Entry"** — your mood is recorded!
5. **Edit** an entry by clicking the ✏️ icon
6. **Delete** an entry by clicking the 🗑️ icon
7. **View your calendar** to see mood patterns
8. **Switch to Dashboard** for analytics charts

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/moods/?user_id=...` | List mood entries |
| `POST` | `/moods/` | Create mood entry |
| `GET` | `/moods/{id}` | Get mood entry by ID |
| `PUT` | `/moods/{id}` | **Update** mood entry |
| `DELETE` | `/moods/{id}` | Delete mood entry |
| `GET` | `/users/` | List users |
| `POST` | `/users/` | Create user |
| `GET` | `/analytics/summary` | Mood summary |
| `GET` | `/analytics/timeline` | Mood timeline |
| `GET` | `/analytics/streak` | Current streak |

---

## Deployment

### Target OS

**Ubuntu 24.04 LTS** (same as university VMs)

### Prerequisites (What Should Be Installed on the VM)

```bash
# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Docker Compose (v2, usually bundled with Docker)
docker compose version
```

### Step-by-Step Instructions

#### 1. Transfer the Code

**Option A — via Git (recommended):**
```bash
git clone <repo-url> ~/se-toolkit-mood-weather
cd ~/se-toolkit-mood-weather
```

**Option B — via SCP:**
```bash
# From your local machine:
scp -r ./se-toolkit-mood-weather user@vm-ip:~/
```

#### 2. Configure Environment Variables

```bash
cd ~/se-toolkit-mood-weather
cp .env.docker.example .env
```

Edit `.env` and **change these values for production**:

```env
MOOD_WEATHER_API_KEY=<generate-a-secure-key>
MOOD_WEATHER_DB_PASSWORD=<strong-password>
POSTGRES_PASSWORD=<same-as-db-password>
PGADMIN_DEFAULT_EMAIL=admin@moodweather.dev
PGADMIN_DEFAULT_PASSWORD=<strong-password>
```

Generate secure keys with:
```bash
openssl rand -hex 32   # for API key
openssl rand -hex 16   # for passwords
```

#### 3. Start the Application

```bash
docker compose up -d --build
```

#### 4. Verify Deployment

```bash
# Check container status
docker compose ps

# Check backend health
curl http://localhost:42001/health
# Expected: {"status":"ok","version":"0.1.0"}

# Check frontend
curl -s -o /dev/null -w '%{http_code}' http://localhost:42002/
# Expected: 200
```

#### 5. Access the Application

| Service | URL |
|---------|-----|
| **Frontend** | `http://<vm-ip>:42002` |
| **API Docs** | `http://<vm-ip>:42002/docs` |
| **Backend API** | `http://<vm-ip>:42001` |
| **PgAdmin** | `http://<vm-ip>:42003` |

#### 6. Configure Firewall (optional)

```bash
sudo ufw allow 42002/tcp   # Frontend
sudo ufw allow 42001/tcp   # Backend (if external access needed)
```

### Useful Commands

```bash
# Stop the application
docker compose down

# Stop and remove all data (warning: deletes database!)
docker compose down -v

# View logs
docker compose logs -f

# Restart a specific service
docker compose restart backend

# Update and redeploy
git pull && docker compose up -d --build
```

---

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

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12, FastAPI, SQLModel, asyncpg |
| **Frontend** | React 18, TypeScript, Vite, Chart.js |
| **Database** | PostgreSQL 18 |
| **Proxy** | Caddy 2 |
| **Testing** | pytest, pytest-asyncio, httpx |
| **Deployment** | Docker Compose, Ubuntu 24.04 VM |

## License

MIT
