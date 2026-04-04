# Domain Model

## Entities

### User

Represents a person using the Mood Weather application.

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| external_id | string | Unique identifier from external system |
| display_name | string | User's display name |
| created_at | datetime | Account creation timestamp |

### MoodEntry

Represents a single mood entry using weather metaphor.

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| user_id | string | Reference to user |
| entry_date | date | Date of the mood entry |
| weather_type | string | Mood as weather: sunny, cloudy, rainy, stormy |
| note | string? | Optional note (max 500 chars) |
| created_at | datetime | Entry creation timestamp |

## Weather Types

| Type | Meaning |
|------|---------|
| sunny | Great mood, feeling positive |
| cloudy | Okay mood, somewhat neutral |
| rainy | Low mood, feeling down |
| stormy | Very bad mood, stressed |

## Constraints

- One mood entry per user per day
- Weather type must be one of the four valid values
- Entry date cannot be in the future
