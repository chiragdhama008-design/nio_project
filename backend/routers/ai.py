"""AI query API — stub with deterministic fallback."""

from fastapi import APIRouter
from models.incidents import AIQuery, AIResponse
from services.sensor_simulator import simulator
from services.risk_engine import calculate_flood_risk, generate_recommendations

router = APIRouter(prefix="/api/ai", tags=["ai"])


def build_context() -> dict:
    """Gather current system state for AI context."""
    zones_data = simulator.get_all_zones_data()
    risks = []
    for zd in zones_data:
        risk = calculate_flood_risk(zd)
        risk["recommendations"] = generate_recommendations(risk)
        risks.append(risk)

    risks.sort(key=lambda r: r["risk_score"], reverse=True)

    return {
        "simulation": simulator.get_state(),
        "zones": risks,
        "overall_risk": risks[0]["risk_score"] if risks else 0,
        "highest_risk_zone": risks[0] if risks else None,
    }


def fallback_response(question: str, context: dict) -> str:
    """Deterministic fallback when no LLM API is available."""
    q = question.lower()
    highest = context.get("highest_risk_zone", {})
    zone_name = highest.get("zone_name", "Unknown")
    score = highest.get("risk_score", 0)
    severity = highest.get("severity", "low")
    factors = highest.get("contributing_factors", {})
    recs = highest.get("recommendations", [])

    if any(w in q for w in ["happening", "status", "situation", "overview"]):
        lines = [f"**Current Situation**\n"]
        if score > 50:
            lines.append(
                f"{zone_name} is experiencing elevated flood risk "
                f"(score: {score}/100, severity: {severity}).\n"
            )
        else:
            lines.append("All zones are operating within normal parameters.\n")

        lines.append(f"**Zone Risk Summary**\n")
        for z in context["zones"][:3]:
            lines.append(f"- {z['zone_name']}: {z['risk_score']}/100 ({z['severity']})")
        return "\n".join(lines)

    if any(w in q for w in ["why", "cause", "factor", "reason"]):
        lines = [f"**Risk Factor Analysis — {zone_name}**\n"]
        lines.append(f"Overall risk score: {score}/100\n")
        lines.append("Contributing factors:")
        for k, v in sorted(factors.items(), key=lambda x: -x[1]):
            lines.append(f"- {k.replace('_', ' ').title()}: +{v}")
        return "\n".join(lines)

    if any(w in q for w in ["do", "action", "recommend", "priority"]):
        lines = [f"**Recommended Actions — {zone_name}**\n"]
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {rec}")
        return "\n".join(lines)

    if any(w in q for w in ["road", "traffic", "route"]):
        td = highest.get("sensor_values", {}).get("traffic_density", 0)
        rh = highest.get("sensor_values", {}).get("road_health", 0)
        lines = [f"**Road & Traffic Status — {zone_name}**\n"]
        lines.append(f"- Traffic density: {td}%")
        lines.append(f"- Road health: {rh}%")
        if td > 60:
            lines.append("\nTraffic is heavily congested. Recommend diversion.")
        if rh < 70:
            lines.append("\nRoad surface conditions are degraded. Caution advised.")
        return "\n".join(lines)

    # Generic
    lines = [f"**UrbanShield System Summary**\n"]
    lines.append(f"Highest risk: {zone_name} — {score}/100 ({severity})")
    lines.append(f"Simulation mode: {context['simulation']['mode']}")
    lines.append(f"\nAsk about specific zones, risk factors, or recommended actions.")
    return "\n".join(lines)


@router.post("/query")
def ai_query(query: AIQuery):
    """Process an AI query about the current city state."""
    context = build_context()

    # For now, use deterministic fallback.
    # LLM integration will be added later.
    answer = fallback_response(query.question, context)

    return AIResponse(answer=answer, context={"mode": "fallback"})
