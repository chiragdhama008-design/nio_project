"""Zones API."""

from fastapi import APIRouter
from models.zones import DEFAULT_ZONES
from services.sensor_simulator import simulator
from services.risk_engine import calculate_flood_risk

router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("")
def get_zones():
    """Return all city zones with current risk levels."""
    zones_data = simulator.get_all_zones_data()
    result = []
    for zone in DEFAULT_ZONES:
        zone_sensor = next(
            (z for z in zones_data if z.zone_id == zone.id), None
        )
        risk = None
        if zone_sensor:
            risk = calculate_flood_risk(zone_sensor)

        result.append({
            **zone.model_dump(),
            "risk_level": risk["severity"] if risk else "normal",
            "risk_score": risk["risk_score"] if risk else 0,
        })
    return {"zones": result}


@router.get("/{zone_id}")
def get_zone(zone_id: str):
    """Return single zone details with sensor data and risk."""
    zone = next((z for z in DEFAULT_ZONES if z.id == zone_id), None)
    if not zone:
        return {"error": "Zone not found"}, 404

    zone_data = simulator.get_zone_data(zone_id)
    risk = calculate_flood_risk(zone_data)

    return {
        "zone": zone.model_dump(),
        "sensors": zone_data.model_dump(),
        "risk": risk,
    }
