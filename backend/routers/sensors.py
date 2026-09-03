"""Sensors API."""

from fastapi import APIRouter
from services.sensor_simulator import simulator, ZONE_NAMES

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("")
def get_sensors():
    """Return current sensor readings for all zones."""
    zones_data = simulator.get_all_zones_data()
    return {
        "zones": [z.model_dump() for z in zones_data],
        "sensor_count": len(zones_data) * 6,
        "status": "online",
    }


@router.get("/{zone_id}")
def get_zone_sensors(zone_id: str):
    """Return sensor readings for a specific zone."""
    if zone_id not in ZONE_NAMES:
        return {"error": "Zone not found"}, 404

    data = simulator.get_zone_data(zone_id)
    return {"sensors": data.model_dump()}
