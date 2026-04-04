# Lab Tasks

## Task 1: Set Up and Explore

**Goal:** Get the application running and explore the codebase.

1. Fork the repository and clone it
2. Copy `.env.docker.example` to `.env`
3. Run `docker compose up --build`
4. Open the application at `http://localhost:42002`
5. Create a user and log your first mood entry
6. Explore the API docs at `http://localhost:42002/docs`

**Deliverable:** Screenshot of the running application with a mood entry.

## Task 2: Add Tests

**Goal:** Write unit tests for the backend.

1. Review the existing test structure in `backend/tests/`
2. Run the existing tests: `uv run --with pytest pytest backend/tests/unit`
3. Add tests for the users endpoint
4. Add edge case tests for mood entries (invalid dates, invalid weather types)

**Deliverable:** All tests passing, with new test files committed.

## Task 3: MCP Integration

**Goal:** Set up the MCP server for agent integration.

1. Review the MCP server code in `mcp/mcp-mood-weather/`
2. Install the MCP server as a tool for your agent
3. Test the tools: `mood_weather_health`, `mood_weather_summary`, `mood_weather_streak`
4. Write a skill prompt that teaches the agent how to use mood weather tools

**Deliverable:** Agent can answer "What's my mood streak?" using MCP tools.

## Task 4: Add a Feature

**Goal:** Extend the application with a new feature.

Choose one:
- **A:** Add mood entry update (PUT endpoint)
- **B:** Add monthly calendar view to the frontend
- **C:** Add export mood data as CSV
- **D:** Add mood insights (e.g., "You tend to be sunny on weekends")

**Deliverable:** Feature implemented with tests and documentation.
