/**
 * API client for UrbanShield backend.
 */

const API_BASE = 'http://localhost:8000';

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  try {
    const res = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`API request failed: ${path}`, err);
    throw err;
  }
}

export const api = {
  // Sensors
  getSensors: () => request('/api/sensors'),

  // Zones
  getZones: () => request('/api/zones'),
  getZone: (zoneId) => request(`/api/zones/${zoneId}`),

  // Risk
  getRisk: () => request('/api/risk'),
  getZoneRisk: (zoneId) => request(`/api/risk/${zoneId}`),

  // Incidents
  getIncidents: () => request('/api/incidents'),

  // Simulation
  startSimulation: () => request('/api/simulation/start', { method: 'POST' }),
  stopSimulation: () => request('/api/simulation/stop', { method: 'POST' }),
  getSimulationStatus: () => request('/api/simulation/status'),

  // AI
  askAI: (question) =>
    request('/api/ai/query', {
      method: 'POST',
      body: JSON.stringify({ question }),
    }),

  // Health
  health: () => request('/api/health'),
};
