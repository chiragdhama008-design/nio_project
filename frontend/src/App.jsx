/**
 * UrbanShield AI — Main Dashboard
 */

import { useCallback } from 'react';
import { api } from './api/client';
import { usePolling } from './hooks/usePolling';
import Header from './components/Header';
import StatusBar from './components/StatusBar';
import ZoneMap from './components/ZoneMap';
import ConditionsPanel from './components/ConditionsPanel';
import IncidentTable from './components/IncidentTable';
import SimulationControls from './components/SimulationControls';
import AIPanel from './components/AIPanel';

function App() {
  const fetchSensors = useCallback(() => api.getSensors(), []);
  const fetchZones = useCallback(() => api.getZones(), []);
  const fetchRisk = useCallback(() => api.getRisk(), []);
  const fetchIncidents = useCallback(() => api.getIncidents(), []);
  const fetchSimStatus = useCallback(() => api.getSimulationStatus(), []);

  const { data: sensors } = usePolling(fetchSensors, 2000);
  const { data: zones } = usePolling(fetchZones, 2000);
  const { data: risk } = usePolling(fetchRisk, 2000);
  const { data: incidents } = usePolling(fetchIncidents, 2000);
  const { data: simulation, refresh: refreshSim } = usePolling(fetchSimStatus, 1000);

  const sensorCount = sensors?.sensor_count ?? 0;
  const backendStatus = sensors ? 'online' : 'offline';

  return (
    <div className="app">
      <Header simulation={simulation} backendStatus={backendStatus} />

      <main className="dashboard">
        <StatusBar risk={risk} incidents={incidents} sensorCount={sensorCount} />

        <div className="dashboard-grid">
          <div className="col-left">
            <ZoneMap zones={zones} />
            <ConditionsPanel sensors={sensors} />
          </div>
          <div className="col-right">
            <SimulationControls simulation={simulation} onRefresh={refreshSim} />
            <IncidentTable incidents={incidents} />
            <AIPanel />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
