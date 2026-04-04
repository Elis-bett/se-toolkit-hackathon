FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml ./

# Create virtual environment and install dependencies
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python fastapi uvicorn sqlmodel asyncpg pydantic pydantic-settings aiosqlite

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

EXPOSE 42001

CMD ["python", "-m", "mood_weather.run"]
