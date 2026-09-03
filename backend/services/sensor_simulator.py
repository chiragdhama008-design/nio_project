"""
Simulated IoT sensor network.

Generates realistic sensor data for 6 city zones.
Supports normal mode and flash-flood emergency simulation.
Values change gradually (not randomly) to create realistic trends.
"""

import random
import time
import math
from datetime import datetime, timezone
from typing import Optional
from models.sensors import ZoneSensorData, SensorReading


# ---------------------------------------------------------------------------
# Normal baseline values per zone
# ---------------------------------------------------------------------------

ZONE_BASELINES = {
    "zone-1": {  # Central District
        "rainfall": 22, "water_level": 30, "drainage_capacity": 94,
        "traffic_density": 55, "air_quality": 72, "road_health": 85,
    },
    "zone-2": {  # Industrial
        "rainfall": 20, "water_level": 28, "drainage_capacity": 88,
        "traffic_density": 40, "air_quality": 58, "road_health": 78,
    },
    "zone-3": {  # Residential
        "rainfall": 25, "water_level": 32, "drainage_capacity": 92,
        "traffic_density": 35, "air_quality": 80, "road_health": 86,
    },
    "zone-4": {  # Riverside (most flood-prone)
        "rainfall": 28, "water_level": 40, "drainage_capacity": 82,
        "traffic_density": 38, "air_quality": 75, "road_health": 80,
    },
    "zone-5": {  # Transit Hub
        "rainfall": 24, "water_level": 33, "drainage_capacity": 90,
        "traffic_density": 65, "air_quality": 65, "road_health": 82,
    },
    "zone-6": {  # Outer Ring
        "rainfall": 22, "water_level": 25, "drainage_capacity": 95,
        "traffic_density": 28, "air_quality": 85, "road_health": 88,
    },
}

# Emergency targets — values deteriorate toward these during flood simulation
FLOOD_TARGETS = {
    "zone-1": {
        "rainfall": 68, "water_level": 55, "drainage_capacity": 58,
        "traffic_density": 70, "air_quality": 60, "road_health": 68,
    },
    "zone-2": {
        "rainfall": 60, "water_level": 48, "drainage_capacity": 62,
        "traffic_density": 55, "air_quality": 50, "road_health": 65,
    },
    "zone-3": {
        "rainfall": 72, "water_level": 60, "drainage_capacity": 52,
        "traffic_density": 68, "air_quality": 65, "road_health": 64,
    },
    "zone-4": {  # Riverside — worst hit
        "rainfall": 88, "water_level": 78, "drainage_capacity": 38,
        "traffic_density": 80, "air_quality": 55, "road_health": 55,
    },
    "zone-5": {
        "rainfall": 75, "water_level": 62, "drainage_capacity": 50,
        "traffic_density": 82, "air_quality": 58, "road_health": 60,
    },
    "zone-6": {
        "rainfall": 55, "water_level": 42, "drainage_capacity": 68,
        "traffic_density": 45, "air_quality": 70, "road_health": 72,
    },
}

ZONE_NAMES = {
    "zone-1": "Central District",
    "zone-2": "Industrial Zone",
    "zone-3": "Residential Area",
    "zone-4": "Riverside",
    "zone-5": "Transit Hub",
    "zone-6": "Outer Ring",
}


class SensorSimulator:
    """Generates sensor data for all zones."""

    def __init__(self):
        self.mode: str = "normal"
        self.flood_progress: float = 0.0  # 0.0 = normal, 1.0 = full emergency
        self.active: bool = False
        self.started_at: Optional[datetime] = None
        self._tick: int = 0

    def start_flood(self):
        self.mode = "flood"
        self.active = True
        self.flood_progress = 0.0
        self.started_at = datetime.now(timezone.utc)

    def stop_flood(self):
        self.mode = "normal"
        self.active = False
        self.flood_progress = 0.0
        self.started_at = None

    def get_state(self) -> dict:
        return {
            "mode": self.mode,
            "active": self.active,
            "progress": round(self.flood_progress, 3),
            "started_at": self.started_at.isoformat() if self.started_at else None,
        }

    def tick(self):
        """Advance the simulation by one step."""
        self._tick += 1
        if self.active and self.mode == "flood":
            # Progress increases over ~30 ticks (30 seconds at 1/sec polling)
            self.flood_progress = min(1.0, self.flood_progress + 0.033)

    def _interpolate(self, baseline: float, target: float, progress: float) -> float:
        """Smoothly interpolate between baseline and target."""
        value = baseline + (target - baseline) * progress
        # Add small realistic noise
        noise = random.gauss(0, 1.2)
        return round(max(0, min(100, value + noise)), 1)

    def get_zone_data(self, zone_id: str) -> ZoneSensorData:
        """Get current sensor readings for a zone."""
        baseline = ZONE_BASELINES.get(zone_id, ZONE_BASELINES["zone-1"])
        target = FLOOD_TARGETS.get(zone_id, FLOOD_TARGETS["zone-1"])

        progress = self.flood_progress if self.mode == "flood" else 0.0

        # Add subtle temporal variation even in normal mode
        t = self._tick * 0.1
        normal_drift = math.sin(t + hash(zone_id) % 10) * 2

        data = {}
        for key in baseline:
            base = baseline[key] + normal_drift
            if key == "drainage_capacity":
                # Drainage goes DOWN under stress (lower = worse)
                data[key] = self._interpolate(base, target[key], progress)
            else:
                data[key] = self._interpolate(base, target[key], progress)

        return ZoneSensorData(
            zone_id=zone_id,
            zone_name=ZONE_NAMES.get(zone_id, zone_id),
            rainfall=data["rainfall"],
            water_level=data["water_level"],
            drainage_capacity=data["drainage_capacity"],
            traffic_density=data["traffic_density"],
            air_quality=data["air_quality"],
            road_health=data["road_health"],
            timestamp=datetime.now(timezone.utc),
        )

    def get_all_zones_data(self) -> list[ZoneSensorData]:
        """Get current readings for all zones."""
        self.tick()
        return [self.get_zone_data(zid) for zid in ZONE_BASELINES]

    def get_readings_list(self) -> list[SensorReading]:
        """Get flat list of individual sensor readings."""
        readings = []
        now = datetime.now(timezone.utc)
        for zone_data in self.get_all_zones_data():
            for field in ["rainfall", "water_level", "drainage_capacity",
                          "traffic_density", "air_quality", "road_health"]:
                unit_map = {
                    "rainfall": "mm/hr", "water_level": "%",
                    "drainage_capacity": "%", "traffic_density": "%",
                    "air_quality": "AQI", "road_health": "%",
                }
                readings.append(SensorReading(
                    sensor_id=f"{zone_data.zone_id}-{field}",
                    zone_id=zone_data.zone_id,
                    type=field,
                    value=getattr(zone_data, field),
                    unit=unit_map[field],
                    timestamp=now,
                ))
        return readings


# Singleton
simulator = SensorSimulator()
