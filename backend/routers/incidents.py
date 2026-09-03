"""Incidents API."""

from fastapi import APIRouter
from datetime import datetime, timezone
from services.sensor_simulator import simulator
from services.risk_engine import calculate_flood_risk, generate_recommendations
import uuid

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


def detect_incidents() -> list[dict]:
    """Detect incidents based on current sensor data and risk scores."""
    zones_data = simulator.get_all_zones_data()
    incidents = []

    for zone_data in zones_data:
        risk = calculate_flood_risk(zone_data)

        # Only create incidents for moderate+ risk
        if risk["risk_score"] < 30:
            continue

        incident = {
            "id": f"inc-{zone_data.zone_id}-flood",
            "type": "flood",
            "zone_id": zone_data.zone_id,
            "zone_name": zone_data.zone_name,
            "severity": risk["severity"],
            "confidence": min(0.95, risk["risk_score"] / 100 + 0.1),
            "risk_score": risk["risk_score"],
            "status": "active",
            "detected_conditions": risk["sensor_values"],
            "contributing_factors": risk["contributing_factors"],
            "recommended_actions": generate_recommendations(risk),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        incidents.append(incident)

    # Sort by risk score descending
    incidents.sort(key=lambda i: i["risk_score"], reverse=True)
    return incidents


@router.get("")
def get_incidents():
    """Return all active incidents."""
    incidents = detect_incidents()
    return {
        "incidents": incidents,
        "total": len(incidents),
    }
