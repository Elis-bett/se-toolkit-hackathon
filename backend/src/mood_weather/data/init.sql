-- Mood Weather database schema
-- This file is used for initializing the database

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mood_entries (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    entry_date DATE NOT NULL,
    weather_type VARCHAR(50) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mood_entries_user_id ON mood_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_mood_entries_entry_date ON mood_entries(entry_date);
CREATE INDEX IF NOT EXISTS idx_users_external_id ON users(external_id);
