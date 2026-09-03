"""Sensor data models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Sensor(BaseModel):
    id: str
    zone_id: str
    type: str
    unit: str
    label: Optional[str] = None
    status: str = "online"
    lat: Optional[float] = None
    lng: Optional[float] = None


class SensorReading(BaseModel):
    sensor_id: str
    zone_id: str
    type: str
    value: float
    unit: str
    timestamp: Optional[datetime] = None


class ZoneSensorData(BaseModel):
    """Aggregated sensor data for a zone."""
    zone_id: str
    zone_name: str
    rainfall: float = 0.0
    water_level: float = 0.0
    drainage_capacity: float = 0.0
    traffic_density: float = 0.0
    air_quality: float = 0.0
    road_health: float = 0.0
    timestamp: Optional[datetime] = None


# Sensor type definitions
SENSOR_TYPES = [
    {"type": "rainfall", "unit": "mm/hr", "label": "Rainfall"},
    {"type": "water_level", "unit": "%", "label": "Water Level"},
    {"type": "drainage_capacity", "unit": "%", "label": "Drainage Capacity"},
    {"type": "traffic_density", "unit": "%", "label": "Traffic Density"},
    {"type": "air_quality", "unit": "AQI", "label": "Air Quality"},
    {"type": "road_health", "unit": "%", "label": "Road Health"},
]


def build_default_sensors() -> list[Sensor]:
    """Create default sensors for all zones."""
    sensors = []
    from models.zones import DEFAULT_ZONES
    for zone in DEFAULT_ZONES:
        for st in SENSOR_TYPES:
            sensors.append(Sensor(
                id=f"{zone.id}-{st['type']}",
                zone_id=zone.id,
                type=st["type"],
                unit=st["unit"],
                label=f"{zone.name} — {st['label']}",
            ))
    return sensors
