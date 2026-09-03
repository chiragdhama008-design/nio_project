"""Risk assessment API."""

from fastapi import APIRouter
from services.sensor_simulator import simulator
from services.risk_engine import calculate_flood_risk, generate_recommendations

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("")
def get_risk():
    """Return risk assessment for all zones."""
    zones_data = simulator.get_all_zones_data()
    results = []
    for zone_data in zones_data:
        risk = calculate_flood_risk(zone_data)
        risk["recommendations"] = generate_recommendations(risk)
        results.append(risk)

    # Sort by risk score descending
    results.sort(key=lambda r: r["risk_score"], reverse=True)

    # Overall risk = max zone risk
    overall = results[0] if results else None

    return {
        "overall_risk": overall["risk_score"] if overall else 0,
        "overall_severity": overall["severity"] if overall else "low",
        "zones": results,
    }


@router.get("/{zone_id}")
def get_zone_risk(zone_id: str):
    """Return risk assessment for a specific zone."""
    zone_data = simulator.get_zone_data(zone_id)
    risk = calculate_flood_risk(zone_data)
    risk["recommendations"] = generate_recommendations(risk)
    return risk
