/**
 * Header — system title, status indicators, simulation state.
 */

import { useState, useEffect } from 'react';

export default function Header({ simulation, backendStatus }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const isFlood = simulation?.mode === 'flood' && simulation?.active;
  const statusColor = backendStatus === 'online' ? 'var(--color-ok)' : 'var(--color-muted)';

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">UrbanShield</h1>
        <span className="header-subtitle">Urban Intelligence &amp; Response</span>
      </div>
      <div className="header-right">
        <div className="header-indicator">
          <span className="indicator-dot" style={{ background: statusColor }} />
          <span className="indicator-label">System {backendStatus ?? 'connecting'}</span>
        </div>
        <div className="header-indicator">
          <span className="indicator-dot" style={{
            background: isFlood ? 'var(--color-critical)' : 'var(--color-ok)'
          }} />
          <span className="indicator-label">
            {isFlood ? 'FLOOD SIMULATION' : 'Normal Operations'}
          </span>
        </div>
        <span className="header-time">{time.toLocaleTimeString()}</span>
      </div>
    </header>
  );
}
