"""
Supabase / PostgreSQL database layer.

When Supabase credentials are available, uses the Supabase client.
Otherwise, provides an in-memory demo data store so the app still runs.
"""

from config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

_supabase_client = None


def get_supabase():
    """Return Supabase client, or None if credentials are missing."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not settings.has_supabase:
        logger.warning(
            "Supabase credentials not configured. Running in demo mode."
        )
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(settings.supabase_url, settings.supabase_key)
        logger.info("Connected to Supabase.")
        return _supabase_client
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        return None


# ---------------------------------------------------------------------------
# In-memory demo store (used when Supabase is unavailable)
# ---------------------------------------------------------------------------

class DemoStore:
    """Simple in-memory store that mirrors the DB tables."""

    def __init__(self):
        self.zones: dict = {}
        self.sensors: dict = {}
        self.sensor_readings: list = []
        self.incidents: dict = {}
        self.recommended_actions: list = []
        self.simulation_events: list = []

    def reset(self):
        self.sensor_readings.clear()
        self.incidents.clear()
        self.recommended_actions.clear()
        self.simulation_events.clear()


demo_store = DemoStore()


def is_demo_mode() -> bool:
    return get_supabase() is None
