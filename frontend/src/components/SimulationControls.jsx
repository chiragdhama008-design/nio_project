/**
 * SimulationControls — toggle between normal and flood simulation modes.
 */

import { api } from '../api/client';

export default function SimulationControls({ simulation, onRefresh }) {
  const isActive = simulation?.active;

  async function handleStart() {
    await api.startSimulation();
    onRefresh?.();
  }

  async function handleStop() {
    await api.stopSimulation();
    onRefresh?.();
  }

  const progress = simulation?.progress ?? 0;

  return (
    <div className="panel simulation-panel">
      <h2 className="panel-title">Simulation Control</h2>
      <div className="sim-controls">
        <button
          className="btn btn-normal"
          onClick={handleStop}
          disabled={!isActive}
        >
          Normal Mode
        </button>
        <button
          className="btn btn-emergency"
          onClick={handleStart}
          disabled={isActive}
        >
          Simulate Flash Flood
        </button>
      </div>
      {isActive && (
        <div className="sim-progress">
          <div className="sim-progress-bar">
            <div
              className="sim-progress-fill"
              style={{ width: `${Math.round(progress * 100)}%` }}
            />
          </div>
          <span className="sim-progress-label">
            Flood progression: {Math.round(progress * 100)}%
          </span>
        </div>
      )}
    </div>
  );
}
