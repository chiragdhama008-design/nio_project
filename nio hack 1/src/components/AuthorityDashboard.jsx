import React from 'react';

export default function AuthorityDashboard({ reports }) {
  // Sort reports by risk score descending
  const sortedReports = [...reports].sort((a, b) => b.aiAnalysis.riskScore - a.aiAnalysis.riskScore);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>CivicShield Authority Dashboard</h2>
        <div className="stats">
          <div className="stat-box">
            <span className="stat-value">{reports.length}</span>
            <span className="stat-label">Total Reports</span>
          </div>
          <div className="stat-box warning">
            <span className="stat-value">{reports.filter(r => r.aiAnalysis.riskScore > 75).length}</span>
            <span className="stat-label">Critical Issues</span>
          </div>
        </div>
      </div>

      {sortedReports.length === 0 ? (
        <p className="empty-state">No hazards reported yet.</p>
      ) : (
        <div className="table-responsive">
          <table className="reports-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Location & Context</th>
                <th>AI Analysis (Computer Vision & NLP)</th>
                <th>Risk Score</th>
              </tr>
            </thead>
            <tbody>
              {sortedReports.map(report => {
                const { aiAnalysis } = report;
                const isCritical = aiAnalysis.riskScore > 75;
                
                return (
                  <tr key={report.id} className={isCritical ? 'critical-row' : ''}>
                    <td>
                      <div className="report-id">{report.id}</div>
                      <div className="timestamp">{new Date(report.timestamp).toLocaleTimeString()}</div>
                      {aiAnalysis.isDuplicate && (
                        <div className="badge duplicate">Duplicate of {aiAnalysis.clusterId}</div>
                      )}
                    </td>
                    <td>
                      <div className="location-text">{report.location}</div>
                      <div className="context-badge">{aiAnalysis.locationContext}</div>
                    </td>
                    <td>
                      <div className="analysis-summary">
                        <strong>{aiAnalysis.hazardType}</strong> ({aiAnalysis.confidence}% conf)
                      </div>
                      <div className="description-snippet">"{report.description}"</div>
                      {aiAnalysis.urgencyKeywords.length > 0 && (
                        <div className="keywords">
                          Keywords: {aiAnalysis.urgencyKeywords.map(kw => <span key={kw} className="keyword-badge">{kw}</span>)}
                        </div>
                      )}
                    </td>
                    <td className="score-cell">
                      <div className={`risk-score ${isCritical ? 'high' : aiAnalysis.riskScore > 40 ? 'medium' : 'low'}`}>
                        {aiAnalysis.riskScore}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
