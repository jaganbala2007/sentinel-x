"""
Sentinel-X Environments: Base Environment Profile Schema
=========================================================
Defines the generic abstraction for all operating environments.
The core safety engine (trust, anomaly, generic risk, autonomous response) remains environment-independent.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SensorSpec(BaseModel):
    sensor_id: str
    parameter: str
    unit: str
    zone: str
    min_limit: float
    max_limit: float
    max_rate_change: float
    default_value: float
    data_source: str = "SIMULATED" # LIVE, SIMULATED, INFERRED, OFFLINE, PLANNED

class HazardRule(BaseModel):
    hazard_id: str
    name: str
    category: str # MECHANICAL, ELECTRICAL, ENVIRONMENTAL, HUMAN, INFRASTRUCTURE
    contributing_parameters: List[str]
    warning_threshold: float
    critical_threshold: float
    severity_weight: float = 1.0

class EnvironmentProfile(BaseModel):
    id: str
    name: str
    type: str # INDUSTRIAL, INDOOR, URBAN, NATURAL, INFRASTRUCTURE, REMOTE, CUSTOM
    location: str
    description: str
    zones: List[str]
    sensors: List[SensorSpec]
    hazards: List[HazardRule]
    risk_weights: Dict[str, float]
    response_rules: Dict[str, str]
    communication_profile: str # "HIGH_BANDWIDTH_ETHERNET", "CELLULAR_MESH", "HF_SATELLITE_HYBRID", etc.
    power_profile: str # "3_PHASE_GRID_UPS", "SOLAR_BATTERY_ISOLATED", etc.
    digital_twin_type: str # "CONVEYOR_3D_SCADA", "FACILITY_BUILDING", "TERRAIN_HYDROLOGY", etc.
