"""AI query API with Groq LLM and deterministic fallback."""

import json

from fastapi import APIRouter
from groq import Groq

from models.incidents import AIQuery, AIResponse
from services.sensor_simulator import simulator
from services.risk_engine import calculate_flood_risk, generate_recommendations
from config import settings

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
    """Deterministic fallback when the LLM is unavailable."""
    q = question.lower()
    highest = context.get("highest_risk_zone", {})

    zone_name = highest.get("zone_name", "Unknown")
    score = highest.get("risk_score", 0)
    severity = highest.get("severity", "low")
    factors = highest.get("contributing_factors", {})
    recs = highest.get("recommendations", [])

    if any(w in q for w in ["happening", "status", "situation", "overview"]):
        lines = ["**Current Situation**\n"]

        if score > 50:
            lines.append(
                f"{zone_name} is experiencing elevated flood risk "
                f"(score: {score}/100, severity: {severity}).\n"
            )
        else:
            lines.append("All zones are operating within normal parameters.\n")

        lines.append("**Zone Risk Summary**\n")

        for z in context["zones"][:3]:
            lines.append(
                f"- {z['zone_name']}: "
                f"{z['risk_score']}/100 ({z['severity']})"
            )

        return "\n".join(lines)

    if any(w in q for w in ["why", "cause", "factor", "reason"]):
        lines = [f"**Risk Factor Analysis — {zone_name}**\n"]
        lines.append(f"Overall risk score: {score}/100\n")
        lines.append("Contributing factors:")

        for k, v in sorted(
            factors.items(),
            key=lambda x: -x[1]
        ):
            lines.append(
                f"- {k.replace('_', ' ').title()}: +{v}"
            )

        return "\n".join(lines)

    if any(w in q for w in ["do", "action", "recommend", "priority"]):
        lines = [f"**Recommended Actions — {zone_name}**\n"]

        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {rec}")

        return "\n".join(lines)

    if any(w in q for w in ["road", "traffic", "route"]):
        sensor_values = highest.get("sensor_values", {})

        td = sensor_values.get("traffic_density", 0)
        rh = sensor_values.get("road_health", 0)

        lines = [f"**Road & Traffic Status — {zone_name}**\n"]
        lines.append(f"- Traffic density: {td}%")
        lines.append(f"- Road health: {rh}%")

        if td > 60:
            lines.append(
                "\nTraffic is heavily congested. Recommend diversion."
            )

        if rh < 70:
            lines.append(
                "\nRoad surface conditions are degraded. "
                "Caution advised."
            )

        return "\n".join(lines)

    return (
        "**UrbanShield System Summary**\n\n"
        f"Highest risk: {zone_name} — {score}/100 ({severity})\n"
        f"Simulation mode: {context['simulation']['mode']}\n\n"
        "Ask about specific zones, risk factors, "
        "or recommended actions."
    )


def llm_response(question: str, context: dict) -> str:
    """Generate an operational response using the Groq LLM."""

    client = Groq(api_key=settings.ai_api_key)

    system_prompt = """
You are UrbanShield AI, an urban emergency intelligence assistant
for a smart-city command center.

Your job is to analyze the CURRENT CITY STATE supplied by the system
and answer the operator's question using only that information.

IMPORTANT RULES:

1. Never invent sensor readings, incidents, locations, or statistics.
2. Treat the supplied risk scores and sensor values as observed system data.
3. The risk engine is responsible for quantitative risk scoring.
4. You are responsible for explaining the situation clearly and
   recommending practical operational actions.
5. If the system is in emergency mode, prioritize urgent actions.
6. Distinguish between observed conditions and recommendations.
7. Keep responses concise and useful to a human city operator.
8. When appropriate, structure responses with short headings,
   bullet points, and numbered actions.
9. If the requested information is not available in the supplied
   context, explicitly say that it is not available.
10. Do not claim that the risk score was produced by an LLM.

You are an assistant for decision support, not an autonomous authority.
Final operational decisions remain with human emergency personnel.
"""

    user_prompt = f"""
CURRENT URBANSHIELD CITY STATE:

{json.dumps(context, indent=2, default=str)}

OPERATOR QUESTION:

{question}

Provide a concise operational response based only on the
current UrbanShield state above.
"""

    response = client.chat.completions.create(
        model=settings.ai_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )

    return response.choices[0].message.content.strip()


@router.post("/query")
def ai_query(query: AIQuery):
    """Process an AI query about the current city state."""

    context = build_context()

    # Use Groq when configured.
    if settings.has_ai and settings.ai_provider.lower() == "groq":
        try:
            answer = llm_response(query.question, context)

            return AIResponse(
                answer=answer,
                context={
                    "mode": "groq",
                    "model": settings.ai_model,
                },
            )

        except Exception as exc:
            print(f"LLM request failed, using fallback: {exc}")

    # Safe fallback if no LLM is configured or the API fails.
    answer = fallback_response(query.question, context)

    return AIResponse(
        answer=answer,
        context={"mode": "fallback"},
    )