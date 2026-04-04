# Architecture

## C4 Model - Context Diagram

```mermaid
graph TB
    User[User: Person tracking mood]
    Browser[Web Browser]
    API[Mood Weather API]
    DB[(PostgreSQL)]

    User -->|Uses| Browser
    Browser -->|HTTP| API
    API -->|Stores| DB
```

## C4 Model - Container Diagram

```mermaid
graph TB
    subgraph "Browser"
        React[React SPA]
    end

    subgraph "Server"
        Caddy[Caddy Reverse Proxy]
        FastAPI[FastAPI Backend]
        Postgres[(PostgreSQL)]
    end

    React -->|API calls| Caddy
    Caddy -->|Proxy| FastAPI
    FastAPI -->|Queries| Postgres
```

## C4 Model - Component Diagram

```mermaid
graph TB
    subgraph "FastAPI Backend"
        RouterMoods[Moods Router]
        RouterUsers[Users Router]
        RouterAnalytics[Analytics Router]
        DBLayer[Database Layer]
        Models[SQLModel Models]
    end

    RouterMoods --> DBLayer
    RouterUsers --> DBLayer
    RouterAnalytics --> DBLayer
    DBLayer --> Models
```

## Sequence Diagram - Create Mood Entry

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database

    U->>F: Select weather icon + date
    F->>A: POST /moods/
    A->>D: Check duplicate
    D-->>A: No duplicate
    A->>D: INSERT mood entry
    D-->>A: Success
    A-->>F: 201 Created
    F-->>U: Show confirmation
```

## Sequence Diagram - View Dashboard

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database

    U->>F: Click Dashboard
    F->>A: GET /analytics/summary
    F->>A: GET /analytics/timeline
    F->>A: GET /analytics/streak
    A->>D: Query aggregations
    D-->>A: Results
    A-->>F: JSON responses
    F-->>U: Render charts
```

## Design Decisions

1. **Monolith backend**: Simple deployment, all endpoints in one FastAPI app
2. **Async database**: asyncpg for better concurrency handling
3. **SQLModel**: Combines Pydantic + SQLAlchemy for cleaner code
4. **Single-origin proxy**: Caddy eliminates CORS issues
5. **Weather metaphor**: 4 simple mood states for low friction tracking
6. **Date uniqueness**: One entry per user per day (enforced at API level)
