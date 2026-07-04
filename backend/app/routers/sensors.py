"""
Sensors & Telemetry Router
===========================
REST API endpoints for IoT sensor data and telemetry aggregation.

Endpoints:
    GET  /api/v1/sensors/telemetry    — Latest aggregated telemetry snapshot
    GET  /api/v1/sensors/{sensor_id}  — Latest reading from a specific sensor
    POST /api/v1/sensors/ingest       — Ingest a new sensor reading (from edge nodes)
    GET  /api/v1/sensors/workers      — All active worker Digital DNA profiles
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import SensorReading, TelemetrySnapshot, WorkerProfile, WorkerLocation

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock telemetry snapshot — replace with Redis cache reads in production
# ---------------------------------------------------------------------------

_MOCK_SNAPSHOT = TelemetrySnapshot(
    timestamp=datetime.utcnow(),
    nodes_synced=1024,
    gas_levels={
        "Zone-A": {"co2_ppm": 310, "h2s_ppm": 0.4, "status": "NORMAL"},
        "Zone-B": {"co2_ppm": 380, "h2s_ppm": 0.8, "status": "NORMAL"},
        "Zone-C": {"co2_ppm": 290, "h2s_ppm": 0.3, "status": "NORMAL"},
        "Zone-D": {"co2_ppm": 340, "h2s_ppm": 0.5, "status": "NORMAL"},
    },
    boiler_temperature={"Boiler-A": {"val": 72.1, "unit": "celsius"}, "Boiler-B": {"val": 74.2, "unit": "celsius"}},
    vibration_hz={"Compressor-B": {"val": 63.4, "unit": "Hz"}, "Pump-A": {"val": 58.1, "unit": "Hz"}},
    noise_db={"Assembly-Floor": {"val": 78.2, "unit": "dB"}, "Compressor-Room": {"val": 84.1, "unit": "dB"}},
    active_worker_count=42,
    risk_score_global=0.8,
)

_MOCK_WORKERS: List[WorkerProfile] = [
    WorkerProfile(
        worker_id="worker-john-doe-01",
        name="John Doe",
        role="Assembly Technician",
        heart_rate_bpm=78,
        spo2_percent=98.0,
        fatigue_coefficient=0.12,
        location=WorkerLocation(x=14.2, y=8.5, z=0.0, zone="Zone-A"),
        ppe_compliant=True,
    ),
    WorkerProfile(
        worker_id="worker-sarah-v-02",
        name="Sarah V.",
        role="Quality Inspector",
        heart_rate_bpm=82,
        spo2_percent=97.5,
        fatigue_coefficient=0.18,
        location=WorkerLocation(x=28.4, y=15.2, z=0.0, zone="Zone-C"),
        ppe_compliant=True,
    ),
    WorkerProfile(
        worker_id="worker-mike-t-03",
        name="Mike T.",
        role="Maintenance Engineer",
        heart_rate_bpm=91,
        spo2_percent=96.8,
        fatigue_coefficient=0.35,
        location=WorkerLocation(x=41.0, y=6.8, z=0.0, zone="Zone-B"),
        ppe_compliant=False,  # PPE violation flagged
    ),
]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/telemetry",
    response_model=TelemetrySnapshot,
    summary="Get Aggregated Telemetry Snapshot",
    description=(
        "Returns the latest multi-sensor telemetry snapshot aggregated "
        "across all 1024 edge nodes. In production, data is read from the "
        "Redis telemetry cache (30s TTL) and falls back to PostgreSQL."
    ),
)
async def get_telemetry_snapshot() -> TelemetrySnapshot:
    """Returns the current live telemetry snapshot."""
    _MOCK_SNAPSHOT.timestamp = datetime.utcnow()
    return _MOCK_SNAPSHOT


@router.get(
    "/workers",
    response_model=List[WorkerProfile],
    summary="Get Active Worker Profiles",
    description=(
        "Returns real-time Digital DNA profiles for all currently active workers, "
        "including UWB position, biometric vitals, PPE compliance, and fatigue score."
    ),
)
async def get_worker_profiles() -> List[WorkerProfile]:
    """Returns all active worker Digital DNA safety profiles."""
    return _MOCK_WORKERS


@router.post(
    "/ingest",
    response_model=dict,
    summary="Ingest Sensor Reading",
    description=(
        "Accepts a single sensor telemetry reading from an edge node. "
        "Data is written to Redis cache and queued for PostgreSQL persistence."
    ),
)
async def ingest_sensor_reading(reading: SensorReading) -> dict:
    """
    Ingestion endpoint called by edge nodes to push new sensor readings.
    In production: validates reading, writes to Redis, publishes MQTT event.
    """
    # Anomaly detection threshold check (simplified)
    thresholds = {"co2": 800.0, "temperature": 85.0, "vibration": 120.0, "noise": 85.0}
    threshold = thresholds.get(reading.sensor_type, float("inf"))
    reading.is_anomaly = reading.value > threshold

    return {
        "status": "ingested",
        "sensor_id": reading.sensor_id,
        "is_anomaly": reading.is_anomaly,
        "timestamp": reading.timestamp.isoformat(),
    }
