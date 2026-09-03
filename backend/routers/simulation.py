"""Simulation control API."""

from fastapi import APIRouter
from services.sensor_simulator import simulator

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


@router.post("/start")
def start_simulation():
    """Start flash flood simulation."""
    simulator.start_flood()
    return {
        "status": "started",
        "mode": "flood",
        "message": "Flash flood simulation initiated.",
    }


@router.post("/stop")
def stop_simulation():
    """Stop simulation, return to normal."""
    simulator.stop_flood()
    return {
        "status": "stopped",
        "mode": "normal",
        "message": "Simulation stopped. Returning to normal conditions.",
    }


@router.get("/status")
def simulation_status():
    """Return current simulation state."""
    return simulator.get_state()
