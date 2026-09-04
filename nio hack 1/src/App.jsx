import React, { useState } from 'react';
import CitizenForm from './components/CitizenForm';
import AuthorityDashboard from './components/AuthorityDashboard';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('citizen'); // 'citizen' or 'dashboard'
  const [reports, setReports] = useState([]);

  const handleReportSubmitted = (newReport) => {
    setReports(prev => [...prev, newReport]);
    // Optionally switch to dashboard to see the result immediately
    // setCurrentView('dashboard'); 
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🛡️ CivicShield</h1>
        <nav>
          <button 
            className={`nav-btn ${currentView === 'citizen' ? 'active' : ''}`}
            onClick={() => setCurrentView('citizen')}
          >
            Citizen Portal
          </button>
          <button 
            className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            Authority Dashboard
          </button>
        </nav>
      </header>

      <main className="app-content">
        {currentView === 'citizen' ? (
          <CitizenForm onReportSubmitted={handleReportSubmitted} />
        ) : (
          <AuthorityDashboard reports={reports} />
        )}
      </main>
    </div>
  );
}

export default App;
