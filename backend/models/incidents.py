"""Incident data models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Incident(BaseModel):
    id: str
    type: str  # flood, traffic, road_hazard, air_quality
    zone_id: str
    severity: str  # low, moderate, high, critical
    confidence: float = 0.0
    risk_score: float = 0.0
    status: str = "active"  # active, monitoring, resolved
    detected_conditions: Optional[dict] = None
    recommended_actions: Optional[list[str]] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class RecommendedAction(BaseModel):
    id: Optional[int] = None
    incident_id: str
    action: str
    priority: int = 0
    status: str = "pending"
    created_at: Optional[datetime] = None


class SimulationState(BaseModel):
    mode: str = "normal"  # normal, flood
    active: bool = False
    progress: float = 0.0  # 0.0 to 1.0
    started_at: Optional[datetime] = None


class AIQuery(BaseModel):
    question: str


class AIResponse(BaseModel):
    answer: str
    context: Optional[dict] = None
