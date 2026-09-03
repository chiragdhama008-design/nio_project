/**
 * StatusBar — compact summary row: overall risk, active incidents, sensors, last update.
 */

export default function StatusBar({ risk, incidents, sensorCount }) {
  const overallRisk = risk?.overall_risk ?? 0;
  const severity = risk?.overall_severity ?? 'low';
  const incidentCount = incidents?.total ?? 0;

  return (
    <div className="status-bar">
      <StatusItem
        label="Overall Risk"
        value={`${Math.round(overallRisk)} / 100`}
        severity={severity}
      />
      <StatusItem
        label="Active Incidents"
        value={incidentCount}
        severity={incidentCount > 0 ? 'warning' : 'normal'}
      />
      <StatusItem
        label="Sensors Online"
        value={sensorCount ?? 36}
        severity="normal"
      />
      <StatusItem
        label="Last Updated"
        value={new Date().toLocaleTimeString()}
        severity="normal"
      />
    </div>
  );
}

function StatusItem({ label, value, severity }) {
  return (
    <div className={`status-item status-${severity}`}>
      <span className="status-label">{label}</span>
      <span className="status-value">{value}</span>
    </div>
  );
}
