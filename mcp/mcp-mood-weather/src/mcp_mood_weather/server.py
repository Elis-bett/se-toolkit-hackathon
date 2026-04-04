"""MCP server implementation for Mood Weather."""

import json
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

from mcp_mood_weather.client import MoodWeatherClient
from mcp_mood_weather.settings import resolve_settings

# Tool definitions
TOOLS = [
    Tool(
        name="mood_weather_health",
        description="Check if the Mood Weather API is healthy",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="mood_weather_get_entries",
        description="Get mood entries for a user",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID"},
                "limit": {
                    "type": "integer",
                    "description": "Number of entries to return",
                    "default": 10,
                },
            },
            "required": ["user_id"],
        },
    ),
    Tool(
        name="mood_weather_log_mood",
        description="Log a mood entry for a user",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID"},
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format",
                },
                "weather_type": {
                    "type": "string",
                    "description": "Weather type: sunny, cloudy, rainy, stormy",
                },
                "note": {
                    "type": "string",
                    "description": "Optional note",
                },
            },
            "required": ["user_id", "date", "weather_type"],
        },
    ),
    Tool(
        name="mood_weather_summary",
        description="Get mood summary for a user",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID"},
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back",
                    "default": 30,
                },
            },
            "required": ["user_id"],
        },
    ),
    Tool(
        name="mood_weather_streak",
        description="Get current streak for a user",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID"},
            },
            "required": ["user_id"],
        },
    ),
    Tool(
        name="mood_weather_timeline",
        description="Get mood timeline for a user",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID"},
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back",
                    "default": 30,
                },
            },
            "required": ["user_id"],
        },
    ),
]


def create_server() -> Server:
    """Create the MCP server instance."""
    settings = resolve_settings()
    client = MoodWeatherClient(settings)

    server = Server("mood-weather")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        try:
            if name == "mood_weather_health":
                result = await client.health_check()
                return [TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))]

            elif name == "mood_weather_get_entries":
                entries = await client.get_mood_entries(
                    user_id=arguments["user_id"],
                    limit=arguments.get("limit", 10),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([e.model_dump() for e in entries], indent=2),
                    )
                ]

            elif name == "mood_weather_log_mood":
                entry = await client.create_mood_entry(
                    user_id=arguments["user_id"],
                    entry_date=arguments["date"],
                    weather_type=arguments["weather_type"],
                    note=arguments.get("note"),
                )
                return [
                    TextContent(
                        type="text", text=json.dumps(entry.model_dump(), indent=2)
                    )
                ]

            elif name == "mood_weather_summary":
                summary = await client.get_summary(
                    user_id=arguments["user_id"],
                    days=arguments.get("days", 30),
                )
                return [
                    TextContent(
                        type="text", text=json.dumps(summary.model_dump(), indent=2)
                    )
                ]

            elif name == "mood_weather_streak":
                streak = await client.get_streak(user_id=arguments["user_id"])
                return [
                    TextContent(
                        type="text", text=json.dumps(streak.model_dump(), indent=2)
                    )
                ]

            elif name == "mood_weather_timeline":
                timeline = await client.get_timeline(
                    user_id=arguments["user_id"],
                    days=arguments.get("days", 30),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([t.model_dump() for t in timeline], indent=2),
                    )
                ]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server


def main():
    """Run the MCP server."""
    server = create_server()
    server.run()
