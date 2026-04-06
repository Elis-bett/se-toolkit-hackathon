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

const DAYS_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

function getCalendarDays(year: number, month: number): (number | null)[][] {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();

  // Monday = 0, Sunday = 6
  let startDay = firstDay.getDay() - 1;
  if (startDay < 0) startDay = 6;

  const weeks: (number | null)[][] = [];
  let currentWeek: (number | null)[] = [];

  // Fill leading nulls
  for (let i = 0; i < startDay; i++) {
    currentWeek.push(null);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    currentWeek.push(day);
    if (currentWeek.length === 7) {
      weeks.push(currentWeek);
      currentWeek = [];
    }
  }

  // Fill trailing nulls
  if (currentWeek.length > 0) {
    while (currentWeek.length < 7) {
      currentWeek.push(null);
    }
    weeks.push(currentWeek);
  }

  return weeks;
}

function App() {
  const [apiKey, setApiKey] = useState<string>(() => localStorage.getItem('mood_api_key') || '');
  const [userId, setUserId] = useState<string>(() => localStorage.getItem('mood_user_id') || '');
  const [authenticated, setAuthenticated] = useState(false);
  const [view, setView] = useState<'tracker' | 'dashboard'>('tracker');

  const [entries, setEntries] = useState<MoodEntry[]>([]);
  const [selectedWeather, setSelectedWeather] = useState('sunny');
  const [note, setNote] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [editingEntryId, setEditingEntryId] = useState<number | null>(null);

  const [calendarMonth, setCalendarMonth] = useState(new Date().getMonth());
  const [calendarYear, setCalendarYear] = useState(new Date().getFullYear());

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

  const handleEditEntry = async (entryId: number, newWeather: string, newNote: string | null) => {
    const baseUrl = import.meta.env.VITE_API_TARGET || '';
    const response = await fetch(`${baseUrl}/moods/${entryId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        weather_type: newWeather,
        note: newNote,
      }),
    });

    if (response.ok) {
      setEditingEntryId(null);
      fetchEntries();
    } else {
      alert('Failed to update mood entry');
    }
  };

  const handleDeleteEntry = async (entryId: number) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;

    const baseUrl = import.meta.env.VITE_API_TARGET || '';
    const response = await fetch(`${baseUrl}/moods/${entryId}`, {
      method: 'DELETE',
    });

    if (response.ok || response.status === 204) {
      fetchEntries();
    } else {
      alert('Failed to delete mood entry');
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
                  const isEditing = editingEntryId === entry.id;

                  return (
                    <div key={entry.id} className="entry-card">
                      <span className="entry-date">{entry.entry_date}</span>
                      {isEditing ? (
                        <div className="entry-edit-form">
                          <select
                            value={weather?.value || 'sunny'}
                            onChange={(e) => {
                              const updatedEntries = entries.map((en) =>
                                en.id === entry.id ? { ...en, weather_type: e.target.value } : en
                              );
                              setEntries(updatedEntries);
                            }}
                          >
                            {WEATHER_OPTIONS.map((opt) => (
                              <option key={opt.value} value={opt.value}>
                                {opt.emoji} {opt.label}
                              </option>
                            ))}
                          </select>
                          <input
                            type="text"
                            value={entry.note || ''}
                            onChange={(e) => {
                              const updatedEntries = entries.map((en) =>
                                en.id === entry.id ? { ...en, note: e.target.value } : en
                              );
                              setEntries(updatedEntries);
                            }}
                            placeholder="Note"
                          />
                          <div className="entry-edit-actions">
                            <button
                              className="btn-save"
                              onClick={() =>
                                handleEditEntry(
                                  entry.id,
                                  entry.weather_type,
                                  entry.note
                                )
                              }
                            >
                              Save
                            </button>
                            <button
                              className="btn-cancel"
                              onClick={() => {
                                setEditingEntryId(null);
                                fetchEntries();
                              }}
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <span className="entry-weather">
                            {weather?.emoji} {weather?.label}
                          </span>
                          {entry.note && <span className="entry-note">{entry.note}</span>}
                          <div className="entry-actions">
                            <button
                              className="btn-edit"
                              onClick={() => setEditingEntryId(entry.id)}
                            >
                              ✏️
                            </button>
                            <button
                              className="btn-delete"
                              onClick={() => handleDeleteEntry(entry.id)}
                            >
                              🗑️
                            </button>
                          </div>
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="mood-calendar">
            <div className="calendar-header">
              <button onClick={() => {
                if (calendarMonth === 0) {
                  setCalendarMonth(11);
                  setCalendarYear(calendarYear - 1);
                } else {
                  setCalendarMonth(calendarMonth - 1);
                }
              }}>◀</button>
              <h3>{MONTH_NAMES[calendarMonth]} {calendarYear}</h3>
              <button onClick={() => {
                if (calendarMonth === 11) {
                  setCalendarMonth(0);
                  setCalendarYear(calendarYear + 1);
                } else {
                  setCalendarMonth(calendarMonth + 1);
                }
              }}>▶</button>
            </div>

            <div className="calendar-grid">
              {DAYS_OF_WEEK.map((day) => (
                <div key={day} className="calendar-day-name">{day}</div>
              ))}

              {getCalendarDays(calendarYear, calendarMonth).flatMap((week, weekIdx) =>
                week.map((day, dayIdx) => {
                  const dateStr = day
                    ? `${calendarYear}-${String(calendarMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
                    : null;
                  const entry = dateStr
                    ? entries.find((e) => e.entry_date === dateStr)
                    : null;
                  const weather = entry
                    ? WEATHER_OPTIONS.find((w) => w.value === entry.weather_type)
                    : null;
                  const isToday =
                    dateStr === new Date().toISOString().split('T')[0];

                  return (
                    <div
                      key={`${weekIdx}-${dayIdx}`}
                      className={`calendar-cell${isToday ? ' today' : ''}${entry ? ' has-entry' : ''}`}
                    >
                      {day ? (
                        <>
                          <span className="calendar-day">{day}</span>
                          {weather && (
                            <span className="calendar-weather" title={weather.label}>
                              {weather.emoji}
                            </span>
                          )}
                        </>
                      ) : null}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      ) : (
        <Dashboard userId={userId} />
      )}
    </div>
  );
}

export default App;
