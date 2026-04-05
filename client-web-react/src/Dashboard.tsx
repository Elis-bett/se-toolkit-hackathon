import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
} from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
);

const WEATHER_LABELS: Record<string, string> = {
  sunny: '☀️ Sunny',
  partly_cloudy: '⛅ Partly Cloudy',
  cloudy: '☁️ Cloudy',
  foggy: '🌫️ Foggy',
  rainy: '🌧️ Rainy',
  snowy: '❄️ Snowy',
  windy: '💨 Windy',
  hail: '🧊 Hail',
  rainbow: '🌈 Rainbow',
  hot: '🔥 Hot',
  freezing: '🥶 Freezing',
  stormy: '⛈️ Stormy',
  tornado: '🌪️ Tornado',
};

const WEATHER_COLORS: Record<string, string> = {
  sunny: '#f6e05e',
  partly_cloudy: '#fbd38d',
  cloudy: '#a0aec0',
  foggy: '#cbd5e0',
  rainy: '#63b3ed',
  snowy: '#e2e8f0',
  windy: '#90cdf4',
  hail: '#b794f4',
  rainbow: '#f687b3',
  hot: '#fc8181',
  freezing: '#90cdf4',
  stormy: '#4a5568',
  tornado: '#718096',
};

interface DashboardProps {
  userId: string;
}

interface SummaryData {
  total_entries: number;
  distribution: Record<string, number>;
}

interface TimelineEntry {
  date: string;
  weather_type: string;
}

interface StreakData {
  current_streak: number;
}

function Dashboard({ userId }: DashboardProps) {
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const baseUrl = import.meta.env.VITE_API_TARGET || '';

      const [summaryRes, timelineRes, streakRes] = await Promise.all([
        fetch(`${baseUrl}/analytics/summary?user_id=${userId}&days=30`),
        fetch(`${baseUrl}/analytics/timeline?user_id=${userId}&days=30`),
        fetch(`${baseUrl}/analytics/streak?user_id=${userId}`),
      ]);

      if (summaryRes.ok) setSummary(await summaryRes.json());
      if (timelineRes.ok) setTimeline(await timelineRes.json());
      if (streakRes.ok) setStreak(await streakRes.json());

      setLoading(false);
    };

    fetchData();
  }, [userId]);

  if (loading) {
    return <div className="dashboard">Loading...</div>;
  }

  const distributionData = summary
    ? {
        labels: Object.keys(summary.distribution).map(
          (key) => WEATHER_LABELS[key] || key,
        ),
        datasets: [
          {
            data: Object.values(summary.distribution),
            backgroundColor: Object.keys(summary.distribution).map(
              (key) => WEATHER_COLORS[key] || '#ccc',
            ),
          },
        ],
      }
    : null;

  const timelineData =
    timeline.length > 0
      ? {
          labels: timeline.map((entry) => entry.date),
          datasets: [
            {
              label: 'Mood',
              data: timeline.map((entry) => {
                const values: Record<string, number> = {
                  sunny: 13,
                  partly_cloudy: 12,
                  cloudy: 11,
                  foggy: 10,
                  rainy: 9,
                  snowy: 8,
                  windy: 7,
                  hail: 6,
                  rainbow: 5,
                  hot: 4,
                  freezing: 3,
                  stormy: 2,
                  tornado: 1,
                };
                return values[entry.weather_type] || 0;
              }),
              borderColor: '#4299e1',
              backgroundColor: 'rgba(66, 153, 225, 0.1)',
              fill: true,
            },
          ],
        }
      : null;

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{summary?.total_entries || 0}</div>
          <div className="stat-label">Total Entries (30 days)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{streak?.current_streak || 0}</div>
          <div className="stat-label">Current Streak</div>
        </div>
      </div>

      {distributionData && (
        <div className="chart-card">
          <h3>Mood Distribution (30 days)</h3>
          <Doughnut data={distributionData} />
        </div>
      )}

      {timelineData && timelineData.labels.length > 0 && (
        <div className="chart-card">
          <h3>Mood Timeline</h3>
          <Line data={timelineData} />
        </div>
      )}

      {!distributionData && !timelineData && (
        <div className="chart-card">
          <p className="empty-state">No data yet. Start tracking your mood!</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
