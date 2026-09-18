"""
Sentinel-X V2 Universal Schemas
================================
Environment-agnostic data contracts for normalized telemetry, environment
profiles, hazard evaluations, and multi-hazard risk fusion.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import time

class EnvironmentType(str, Enum):
    NATURAL_OUTDOOR = "NATURAL_OUTDOOR"
    URBAN_OUTDOOR = "URBAN_OUTDOOR"
    INDOOR_BUILDING = "INDOOR_BUILDING"
    INDUSTRIAL = "INDUSTRIAL"
    CRITICAL_INFRASTRUCTURE = "CRITICAL_INFRASTRUCTURE"
    REMOTE_DISASTER_ZONE = "REMOTE_DISASTER_ZONE"
    CUSTOM = "CUSTOM"

class HazardType(str, Enum):
    FLOOD = "FLOOD"
    FLASH_FLOOD = "FLASH_FLOOD"
    FIRE = "FIRE"
    SMOKE = "SMOKE"
    GAS_LEAK = "GAS_LEAK"
    STRUCTURAL_ANOMALY = "STRUCTURAL_ANOMALY"
    LANDSLIDE = "LANDSLIDE"
    EARTHQUAKE = "EARTHQUAKE"
    EXTREME_HEAT = "EXTREME_HEAT"
    POWER_FAILURE = "POWER_FAILURE"
    EQUIPMENT_FAILURE = "EQUIPMENT_FAILURE"

class SeverityLevel(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class TrustStatus(str, Enum):
    VERIFIED = "VERIFIED"
    TRUSTED = "TRUSTED"
    SUSPICIOUS = "SUSPICIOUS"
    DEGRADED = "DEGRADED"
    QUARANTINED = "QUARANTINED"

class LocationModel(BaseModel):
    # For outdoor environments (GPS)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_m: Optional[float] = None
    # For indoor / industrial environments (Topological)
    building_id: Optional[str] = None
    floor_level: Optional[int] = None
    room_or_zone: Optional[str] = None

class NormalizedSensorReading(BaseModel):
    reading_id: Optional[str] = None
    node_id: str = Field(..., example="NODE-01")
    sequence_num: int = Field(default=1)
    timestamp_ms: int = Field(default_factory=lambda: int(time.time() * 1000))
    sensor_type: str = Field(..., example="ultrasonic_depth")
    metric_name: str = Field(..., example="water_level_m")
    value: float = Field(..., example=2.45)
    unit: str = Field(..., example="m")
    location: Optional[LocationModel] = None
    battery_pct: int = Field(default=95, ge=0, le=100)
    signal_quality_dbm: int = Field(default=-65)
    hardware_health: str = Field(default="HEALTHY")
    confidence: float = Field(default=0.98, ge=0.0, le=1.0)
    auxiliary_metrics: Dict[str, float] = Field(default_factory=dict)

class SensorDefinition(BaseModel):
    sensor_type: str
    metric_name: str
    unit: str
    min_plausible: float
    max_plausible: float
    max_rate_of_change: float # per minute
    warning_threshold: float
    critical_threshold: float
    is_primary: bool = False

class HazardAssessment(BaseModel):
    hazard_type: HazardType
    risk_score: int = Field(..., ge=0, le=100)
    confidence: int = Field(..., ge=0, le=100)
    severity: SeverityLevel
    primary_metric: str
    primary_value: float
    evidence: List[str] = Field(default_factory=list)
    affected_zone: str
    recommended_action: str

class EnvironmentProfile(BaseModel):
    id: EnvironmentType
    name: str
    description: str
    active_hazards: List[HazardType]
    sensor_definitions: List[SensorDefinition]
    communication_priority: List[str] = ["INTERNET", "HF_PACKET", "SATELLITE", "OFFLINE"]
    spatial_reference: str # "GEOGRAPHIC_GIS" or "TOPOLOGICAL_BUILDING"
    primary_response_actions: List[str]
    autonomous_siren_enabled: bool = True

class MultiHazardRiskAssessment(BaseModel):
    environment: EnvironmentType
    overall_risk_score: int = Field(..., ge=0, le=100)
    overall_confidence: int = Field(..., ge=0, le=100)
    overall_severity: SeverityLevel
    primary_threat: HazardType
    active_hazard_assessments: List[HazardAssessment]
    contributing_factors: Dict[str, int]
    evidence_chain: List[str]
    affected_sector: str
    recommended_operational_action: str
    timestamp_ms: int = Field(default_factory=lambda: int(time.time() * 1000))
