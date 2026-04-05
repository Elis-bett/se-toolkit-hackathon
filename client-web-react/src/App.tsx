import { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './Dashboard';

interface MoodEntry {
  id: number;
  user_id: string;
  entry_date: string;
  weather_type: string;
  note: string | null;
  created_at: string;
}

const WEATHER_OPTIONS = [
  { value: 'sunny', label: 'Sunny', emoji: '☀️' },
  { value: 'partly_cloudy', label: 'Partly Cloudy', emoji: '⛅' },
  { value: 'cloudy', label: 'Cloudy', emoji: '☁️' },
  { value: 'foggy', label: 'Foggy', emoji: '🌫️' },
  { value: 'rainy', label: 'Rainy', emoji: '🌧️' },
  { value: 'snowy', label: 'Snowy', emoji: '❄️' },
  { value: 'windy', label: 'Windy', emoji: '💨' },
  { value: 'hail', label: 'Hail', emoji: '🧊' },
  { value: 'rainbow', label: 'Rainbow', emoji: '🌈' },
  { value: 'hot', label: 'Hot', emoji: '🔥' },
  { value: 'freezing', label: 'Freezing', emoji: '🥶' },
  { value: 'stormy', label: 'Stormy', emoji: '⛈️' },
  { value: 'tornado', label: 'Tornado', emoji: '🌪️' },
];

function App() {
  const [apiKey, setApiKey] = useState<string>(() => localStorage.getItem('mood_api_key') || '');
  const [userId, setUserId] = useState<string>(() => localStorage.getItem('mood_user_id') || '');
  const [authenticated, setAuthenticated] = useState(false);
  const [view, setView] = useState<'tracker' | 'dashboard'>('tracker');

  const [entries, setEntries] = useState<MoodEntry[]>([]);
  const [selectedWeather, setSelectedWeather] = useState('sunny');
  const [note, setNote] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    if (apiKey) {
      localStorage.setItem('mood_api_key', apiKey);
    }
    if (userId) {
      localStorage.setItem('mood_user_id', userId);
    }
  }, [apiKey, userId]);

  const handleLogin = () => {
    if (apiKey && userId) {
      setAuthenticated(true);
      fetchEntries();
    }
  };

  const fetchEntries = async () => {
    const baseUrl = import.meta.env.VITE_API_TARGET || '';
    const response = await fetch(`${baseUrl}/moods/?user_id=${userId}&limit=100`);
    if (response.ok) {
      const data = await response.json();
      setEntries(data);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const baseUrl = import.meta.env.VITE_API_TARGET || '';
    const response = await fetch(`${baseUrl}/moods/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        entry_date: selectedDate,
        weather_type: selectedWeather,
        note: note || null,
      }),
    });

    if (response.ok || response.status === 409) {
      setNote('');
      fetchEntries();
    } else {
      alert('Failed to save mood entry');
    }
  };

  if (!authenticated) {
    return (
      <div className="login-container">
        <h1>🌤️ Mood Weather</h1>
        <p>Track your mood as weather</p>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
          className="login-form"
        >
          <input
            type="text"
            placeholder="User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <input
            type="password"
            placeholder="API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
          <button type="submit">Start Tracking</button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌤️ Mood Weather</h1>
        <nav>
          <button className={view === 'tracker' ? 'active' : ''} onClick={() => setView('tracker')}>
            Tracker
          </button>
          <button className={view === 'dashboard' ? 'active' : ''} onClick={() => setView('dashboard')}>
            Dashboard
          </button>
        </nav>
      </header>

      {view === 'tracker' ? (
        <div className="tracker-view">
          <form onSubmit={handleSubmit} className="mood-form">
            <h2>How's your weather today?</h2>

            <div className="date-picker">
              <label>Date:</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>

            <div className="weather-selector">
              {WEATHER_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  className={`weather-option ${selectedWeather === option.value ? 'selected' : ''}`}
                  onClick={() => setSelectedWeather(option.value)}
                >
                  <span className="emoji">{option.emoji}</span>
                  <span className="label">{option.label}</span>
                </button>
              ))}
            </div>

            <textarea
              placeholder="Add a note (optional)"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              maxLength={500}
            />

            <button type="submit" className="submit-btn">
              Save Entry
            </button>
          </form>

          <div className="recent-entries">
            <h3>Recent Entries</h3>
            {entries.length === 0 ? (
              <p className="empty-state">No entries yet. Start tracking your mood!</p>
            ) : (
              <div className="entries-list">
                {entries.slice(0, 10).map((entry) => {
                  const weather = WEATHER_OPTIONS.find((w) => w.value === entry.weather_type);
                  return (
                    <div key={entry.id} className="entry-card">
                      <span className="entry-date">{entry.entry_date}</span>
                      <span className="entry-weather">
                        {weather?.emoji} {weather?.label}
                      </span>
                      {entry.note && <span className="entry-note">{entry.note}</span>}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      ) : (
        <Dashboard userId={userId} />
      )}
    </div>
  );
}

export default App;
