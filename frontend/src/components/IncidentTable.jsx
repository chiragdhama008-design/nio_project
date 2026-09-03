/**
 * IncidentTable — list of active incidents.
 */

export default function IncidentTable({ incidents }) {
  const list = incidents?.incidents ?? [];

  if (list.length === 0) {
    return (
      <div className="panel">
        <h2 className="panel-title">Active Incidents</h2>
        <p className="empty-state">No active incidents detected.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h2 className="panel-title">Active Incidents ({list.length})</h2>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Zone</th>
              <th>Severity</th>
              <th>Risk</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {list.map(inc => (
              <tr key={inc.id}>
                <td className="cell-type">{inc.type}</td>
                <td>{inc.zone_name}</td>
                <td>
                  <span className={`severity-badge severity-${inc.severity}`}>
                    {inc.severity}
                  </span>
                </td>
                <td className="cell-mono">{Math.round(inc.risk_score)}</td>
                <td>
                  <span className={`status-badge status-${inc.status}`}>
                    {inc.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
