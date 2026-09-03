"""Zone data models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Zone(BaseModel):
    id: str
    name: str
    type: str
    description: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    risk_level: str = "normal"
    status: str = "active"
    created_at: Optional[datetime] = None


# Default city zones
DEFAULT_ZONES: list[Zone] = [
    Zone(
        id="zone-1",
        name="Central District",
        type="central",
        description="Downtown business and commercial core",
        lat=28.6139, lng=77.2090,
        risk_level="normal",
    ),
    Zone(
        id="zone-2",
        name="Industrial Zone",
        type="industrial",
        description="Manufacturing and heavy industry area",
        lat=28.6300, lng=77.2200,
        risk_level="normal",
    ),
    Zone(
        id="zone-3",
        name="Residential Area",
        type="residential",
        description="Primary residential neighborhoods",
        lat=28.6000, lng=77.2000,
        risk_level="normal",
    ),
    Zone(
        id="zone-4",
        name="Riverside",
        type="riverside",
        description="Low-lying area near the river, flood-prone",
        lat=28.6200, lng=77.2400,
        risk_level="normal",
    ),
    Zone(
        id="zone-5",
        name="Transit Hub",
        type="transit",
        description="Major transit interchange and station area",
        lat=28.6400, lng=77.2100,
        risk_level="normal",
    ),
    Zone(
        id="zone-6",
        name="Outer Ring",
        type="outer",
        description="Peripheral urban area, mixed use",
        lat=28.5900, lng=77.2300,
        risk_level="normal",
    ),
]
