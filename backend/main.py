"""
UrbanShield AI — FastAPI Backend

Smart-city command center backend providing:
- Simulated IoT sensor data
- Quantitative risk assessment
- Incident detection
- AI query interface
- Simulation controls
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import is_demo_mode
from routers import zones, sensors, risk, incidents, simulation, ai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    mode = "DEMO" if is_demo_mode() else "SUPABASE"
    logger.info(f"UrbanShield AI starting in {mode} mode")
    logger.info(f"AI provider: {settings.ai_provider}")
    yield
    logger.info("UrbanShield AI shutting down")


app = FastAPI(
    title="UrbanShield AI",
    description="Urban Intelligence & Emergency Response Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(zones.router)
app.include_router(sensors.router)
app.include_router(risk.router)
app.include_router(incidents.router)
app.include_router(simulation.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "name": "UrbanShield AI",
        "version": "0.1.0",
        "status": "online",
        "mode": "demo" if is_demo_mode() else "production",
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "demo" if is_demo_mode() else "production"}
