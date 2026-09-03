"""
Explainable quantitative risk engine.

Calculates flood risk using weighted scoring.
This is a rule-based/weighted scoring system, NOT a trained ML model.

Returns risk score (0-100), severity, and contributing factors with
individual point contributions for full explainability.
"""

from models.sensors import ZoneSensorData


# Weight configuration for flood risk factors
FLOOD_WEIGHTS = {
    "rainfall": 0.28,
    "water_level": 0.25,
    "drainage_stress": 0.22,
    "traffic_exposure": 0.15,
    "road_condition": 0.10,
}


def calculate_flood_risk(data: ZoneSensorData) -> dict:
    """
    Calculate flood risk score for a zone based on current sensor data.

    Each factor is normalized to 0-100, multiplied by its weight,
    then summed to produce an overall risk score.

    Returns:
        dict with risk_score, severity, contributing_factors, zone info.
    """

    # --- Individual factor scores (0-100 scale) ---

    # Rainfall: higher = worse. Threshold at ~20mm/hr normal, 80+ severe.
    rainfall_score = min(100, max(0, (data.rainfall - 15) / 0.75))

    # Water level: higher = worse. Already in %.
    water_level_score = min(100, max(0, data.water_level * 1.3))

    # Drainage stress: lower capacity = higher risk.
    drainage_stress_score = min(100, max(0, (100 - data.drainage_capacity) * 1.8))

    # Traffic exposure: higher density = more people at risk.
    traffic_score = min(100, max(0, data.traffic_density * 1.1))

    # Road condition: lower health = more vulnerable.
    road_score = min(100, max(0, (100 - data.road_health) * 1.5))

    # --- Weighted contributions ---
    contributions = {
        "rainfall": round(rainfall_score * FLOOD_WEIGHTS["rainfall"], 1),
        "water_level": round(water_level_score * FLOOD_WEIGHTS["water_level"], 1),
        "drainage_stress": round(drainage_stress_score * FLOOD_WEIGHTS["drainage_stress"], 1),
        "traffic_exposure": round(traffic_score * FLOOD_WEIGHTS["traffic_exposure"], 1),
        "road_condition": round(road_score * FLOOD_WEIGHTS["road_condition"], 1),
    }

    risk_score = round(sum(contributions.values()), 1)
    risk_score = min(100, max(0, risk_score))

    # --- Severity thresholds ---
    if risk_score >= 75:
        severity = "critical"
    elif risk_score >= 50:
        severity = "high"
    elif risk_score >= 30:
        severity = "moderate"
    else:
        severity = "low"

    return {
        "zone_id": data.zone_id,
        "zone_name": data.zone_name,
        "risk_score": risk_score,
        "severity": severity,
        "contributing_factors": contributions,
        "sensor_values": {
            "rainfall": data.rainfall,
            "water_level": data.water_level,
            "drainage_capacity": data.drainage_capacity,
            "traffic_density": data.traffic_density,
            "road_health": data.road_health,
        },
        "method": "weighted_scoring",
        "note": "Rule-based weighted scoring. Not a trained ML model.",
    }


def get_severity_label(score: float) -> str:
    if score >= 75:
        return "critical"
    elif score >= 50:
        return "high"
    elif score >= 30:
        return "moderate"
    return "low"


def generate_recommendations(risk_result: dict) -> list[str]:
    """Generate recommended actions based on risk assessment."""
    score = risk_result["risk_score"]
    severity = risk_result["severity"]
    factors = risk_result["contributing_factors"]

    actions = []

    if severity == "critical":
        actions.append("Issue immediate flood warning for affected zone")
        actions.append("Activate emergency response team")
        actions.append("Close affected roads to non-emergency traffic")

    if severity in ("critical", "high"):
        actions.append("Dispatch drainage maintenance crews")
        actions.append("Redirect traffic through alternate routes")

    if factors.get("rainfall", 0) > 15:
        actions.append("Increase rainfall monitoring frequency")

    if factors.get("water_level", 0) > 15:
        actions.append("Monitor water levels at 1-minute intervals")

    if factors.get("drainage_stress", 0) > 12:
        actions.append("Inspect and clear drainage infrastructure")

    if factors.get("traffic_exposure", 0) > 10:
        actions.append("Alert commuters via traffic management system")

    if factors.get("road_condition", 0) > 5:
        actions.append("Schedule road surface inspection")

    if severity == "moderate":
        actions.append("Place response teams on standby")

    if not actions:
        actions.append("Continue routine monitoring")

    return actions
