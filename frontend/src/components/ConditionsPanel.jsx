/**
 * ConditionsPanel — current sensor conditions with small trend indicators.
 */

import {
  LineChart, Line, ResponsiveContainer,
} from 'recharts';
import { useState, useEffect } from 'react';

// Keep a rolling history for mini sparklines
const MAX_HISTORY = 20;

export default function ConditionsPanel({ sensors }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!sensors?.zones) return;

    // Average across all zones for the overview
    const zones = sensors.zones;
    const avg = (field) => {
      const sum = zones.reduce((s, z) => s + (z[field] ?? 0), 0);
      return Math.round((sum / zones.length) * 10) / 10;
    };

    const point = {
      rainfall: avg('rainfall'),
      water_level: avg('water_level'),
      drainage_capacity: avg('drainage_capacity'),
      traffic_density: avg('traffic_density'),
      air_quality: avg('air_quality'),
      road_health: avg('road_health'),
    };

    setHistory(prev => {
      const next = [...prev, point];
      return next.length > MAX_HISTORY ? next.slice(-MAX_HISTORY) : next;
    });
  }, [sensors]);

  const metrics = [
    { key: 'rainfall', label: 'Rainfall', unit: 'mm/hr', warn: 50 },
    { key: 'water_level', label: 'Water Level', unit: '%', warn: 55 },
    { key: 'drainage_capacity', label: 'Drainage', unit: '%', warn: 60, invert: true },
    { key: 'traffic_density', label: 'Traffic', unit: '%', warn: 60 },
    { key: 'air_quality', label: 'Air Quality', unit: 'AQI', warn: 60, invert: true },
    { key: 'road_health', label: 'Road Health', unit: '%', warn: 70, invert: true },
  ];

  const latest = history[history.length - 1] ?? {};

  return (
    <div className="panel">
      <h2 className="panel-title">Current Conditions</h2>
      <div className="conditions-grid">
        {metrics.map(m => {
          const val = latest[m.key] ?? 0;
          const isWarning = m.invert ? val < m.warn : val > m.warn;

          return (
            <div key={m.key} className="condition-item">
              <div className="condition-header">
                <span className="condition-label">{m.label}</span>
                <span className={`condition-value ${isWarning ? 'condition-warning' : ''}`}>
                  {val} <small>{m.unit}</small>
                </span>
              </div>
              <div className="condition-chart">
                <ResponsiveContainer width="100%" height={32}>
                  <LineChart data={history}>
                    <Line
                      type="monotone"
                      dataKey={m.key}
                      stroke={isWarning ? 'var(--color-warning)' : 'var(--color-info)'}
                      strokeWidth={1.5}
                      dot={false}
                      isAnimationActive={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
