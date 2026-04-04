# Vision Statement

## Product Idea

Users pick a weather icon each day (sunny, cloudy, rainy, stormy) to represent their mood, creating a personal "weather calendar" that's easy to understand at a glance.

## Actors

| Actor | Description |
|-------|-------------|
| User | Person who tracks their daily mood |
| Admin | System administrator managing the application |

## Features

### F1: User Management
- Create and list users
- Users identified by external ID

### F2: Mood Entry Creation
- Create one mood entry per day per user
- Select from 4 weather types: sunny, cloudy, rainy, stormy
- Optional note (max 500 characters)

### F3: Mood Entry Listing
- View recent mood entries for a user
- Ordered by date (newest first)
- Pagination support

### F4: Mood Entry Deletion
- Delete a mood entry by ID

### F5: Mood Summary
- View mood distribution over past N days
- Count of each weather type

### F6: Mood Timeline
- View mood entries as a timeline
- Ordered by date (oldest first)

### F7: Streak Tracking
- Calculate current streak of consecutive days
- Reset streak if a day is missed

### F8: Analytics Dashboard
- Visual charts for mood distribution
- Visual timeline chart
- Streak display

### F9: API Health Check
- Simple endpoint to verify API status

### F10: MCP Server
- Model Context Protocol server for agent integration
- Tools for health, entries, summary, streak, timeline

## Scope

### In Scope
- Single-user mood tracking
- Weather-based mood metaphor
- Basic analytics
- Web interface
- REST API
- MCP server for agent integration

### Out of Scope (Future)
- Multi-user sharing
- Social features
- Reminders/notifications
- Export/import data
- Custom mood types
- Multiple entries per day

## Quality Attributes

| Attribute | Description |
|-----------|-------------|
| Simplicity | One tap per day to log mood |
| Reliability | Data persisted, API is available |
| Testability | Unit tests for all endpoints |
| Deployability | Docker Compose for single-command deploy |
| Maintainability | Clean architecture, typed code |
