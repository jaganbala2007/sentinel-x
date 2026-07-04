"""
Sentinel-X Pydantic Schemas
============================
Data transfer objects (DTOs) and validation schemas for all API endpoints.

These schemas define the shape of request bodies, response payloads,
and internal data structures using Pydantic v2.

Modules:
  - AlertSchema       : Safety alert event structure
  - SensorReading     : IoT sensor telemetry payload
  - TelemetrySnapshot : Aggregated multi-sensor snapshot
  - MachineLockout    : PLC lockout command and response
  - WorkerProfile     : Digital DNA worker profile
  - RiskField         : Dynamic risk field grid state
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class AlertSeverity(str, Enum):
    """Severity levels for safety alerts, ordered by criticality."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertTriggerSource(str, Enum):
    """Source subsystem that generated an alert."""
    VISION_AI = "VISION_AI"
    PREDICTION_AI = "PREDICTION_AI"
    SENSOR_THRESHOLD = "SENSOR_THRESHOLD"
    OPERATOR_MANUAL = "OPERATOR_MANUAL"
    WEARABLE_SOS = "WEARABLE_SOS"


class MachineStatus(str, Enum):
    """Operational state of an industrial machine."""
    NOMINAL = "NOMINAL"
    WARNING = "WARNING"
    LOCKED_OUT = "LOCKED_OUT"
    MAINTENANCE = "MAINTENANCE"


# ---------------------------------------------------------------------------
# Alert Schemas
# ---------------------------------------------------------------------------


class AlertSchema(BaseModel):
    """Represents a single safety alert event."""

    id: str = Field(..., description="Unique alert identifier (e.g. alert-942861)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: AlertSeverity
    trigger_source: AlertTriggerSource
    zone: str = Field(..., description="Factory zone identifier (e.g. Zone-B)")
    details: str = Field(..., description="Human-readable alert description")
    worker_id: Optional[str] = Field(None, description="Associated worker ID if applicable")
    acknowledged: bool = Field(default=False)
    acknowledged_by: Optional[str] = None

    model_config = {"json_schema_extra": {
        "example": {
            "id": "alert-942861",
            "timestamp": "2026-07-01T15:43:09Z",
            "severity": "CRITICAL",
            "trigger_source": "VISION_AI",
            "zone": "Zone-B",
            "details": "Unauthorized worker intrusion into restricted compressor area.",
            "worker_id": "worker-john-doe-01",
            "acknowledged": False,
        }
    }}


class AlertListResponse(BaseModel):
    """Paginated list of alerts."""
    total: int
    alerts: List[AlertSchema]


# ---------------------------------------------------------------------------
# Sensor & Telemetry Schemas
# ---------------------------------------------------------------------------


class SensorReading(BaseModel):
    """A single sensor reading from an IoT node."""

    sensor_id: str = Field(..., description="Unique sensor identifier")
    sensor_type: str = Field(..., description="Type: co2, temperature, vibration, noise")
    value: float = Field(..., description="Measured sensor value")
    unit: str = Field(..., description="Measurement unit: ppm, celsius, Hz, dB")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    zone: str = Field(..., description="Factory zone of this sensor")
    is_anomaly: bool = Field(default=False)

    model_config = {"json_schema_extra": {
        "example": {
            "sensor_id": "CO2_SENSOR_024",
            "sensor_type": "co2",
            "value": 380.0,
            "unit": "ppm",
            "zone": "Zone-A",
            "is_anomaly": False,
        }
    }}


class TelemetrySnapshot(BaseModel):
    """Aggregated multi-sensor snapshot at a point in time."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    nodes_synced: int = Field(..., description="Number of edge nodes reporting")
    gas_levels: Dict[str, Any] = Field(
        ..., description="Gas sensor readings keyed by zone"
    )
    boiler_temperature: Dict[str, Any]
    vibration_hz: Dict[str, Any]
    noise_db: Dict[str, Any]
    active_worker_count: int
    risk_score_global: float = Field(
        ..., ge=0.0, le=100.0, description="Aggregated plant-wide risk percentage"
    )


# ---------------------------------------------------------------------------
# Machine Control Schemas
# ---------------------------------------------------------------------------


class MachineLockoutRequest(BaseModel):
    """Request body for issuing a PLC machine lockout command."""

    machine_id: str = Field(..., description="Target PLC machine identifier")
    operator_id: str = Field(..., description="Operator issuing the lockout")
    reason: str = Field(..., description="Reason for the lockout command")
    emergency_override: bool = Field(
        default=False,
        description="If True, bypasses confirmation delay for emergency stops",
    )

    model_config = {"json_schema_extra": {
        "example": {
            "machine_id": "PLC_COMPRESSOR_B",
            "operator_id": "admin@sentinel.x",
            "reason": "YOLOv11 detected unauthorized worker in compressor zone.",
            "emergency_override": True,
        }
    }}


class MachineLockoutResponse(BaseModel):
    """Response confirming a PLC lockout was executed."""

    status: str
    locked_units: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operator: str
    latency_ms: float = Field(..., description="Time taken to execute lockout in ms")


# ---------------------------------------------------------------------------
# Worker / Digital DNA Schemas
# ---------------------------------------------------------------------------


class WorkerLocation(BaseModel):
    """UWB-derived 3D indoor position."""
    x: float
    y: float
    z: float = 0.0
    zone: str


class WorkerProfile(BaseModel):
    """Real-time Digital DNA safety profile for a single worker."""

    worker_id: str
    name: str
    role: str
    heart_rate_bpm: int = Field(..., ge=30, le=220)
    spo2_percent: float = Field(..., ge=50.0, le=100.0)
    fatigue_coefficient: float = Field(
        ..., ge=0.0, le=1.0,
        description="0.0=alert, 1.0=critically fatigued"
    )
    location: WorkerLocation
    ppe_compliant: bool
    last_updated: datetime = Field(default_factory=datetime.utcnow)
