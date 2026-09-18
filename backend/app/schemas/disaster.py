"""
Pydantic Schemas for Sentinel-X Disaster Resilience Subsystems
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SensorReadingSchema(BaseModel):
    node_id: str = Field(..., example="NODE-01")
    sequence_num: int = Field(..., example=1042)
    timestamp_ms: int = Field(..., example=1725720000000)
    water_level_m: float = Field(..., example=2.41)
    rate_of_rise_m_min: float = Field(..., example=0.01)
    baro_pressure_hpa: Optional[float] = 1013.2
    temperature_c: Optional[float] = 26.4
    soil_saturation_pct: Optional[float] = 48.5
    battery_pct: int = Field(..., example=94)
    safety_state: int = Field(default=0, example=0)
    confidence: float = Field(default=0.98, example=0.98)

class SensorTrustSchema(BaseModel):
    node_id: str
    trust_score: float = Field(..., ge=0.0, le=100.0)
    status: str = Field(..., example="VERIFIED") # VERIFIED, SUSPICIOUS, DEGRADED, QUARANTINED
    reasons: List[str] = Field(default_factory=list)
    temporal_variance: float = 0.02
    consensus_correlation: float = 0.96

class XAIFactorsSchema(BaseModel):
    water: int = 5
    rise: int = 3
    rain: int = 4
    soil: int = 2
    consensus: int = 3
    hist: int = 1

class DisasterRiskSchema(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    confidence: int = Field(..., ge=0, le=100)
    severity: str = Field(..., example="NORMAL") # NORMAL, WATCH, WARNING, CRITICAL
    contributing_factors: XAIFactorsSchema
    evidence: List[str] = Field(default_factory=list)
    affected_sector: str = "SECTOR B (BASIN 04)"
    recommended_action: str = "CONTINUE STEADY MONITORING"

class CommsStatusSchema(BaseModel):
    mode: str = "NORMAL" # NORMAL, DEGRADED, EMERGENCY, ISOLATED
    active_channel: str = "INTERNET"
    internet_status: str = "ONLINE"
    hf_status: str = "STANDBY"
    satellite_status: str = "STANDBY"
    store_and_forward_status: str = "READY"
    queued_events_count: int = 0
    hf_frequency_mhz: float = 7.105

class OfflineEventSchema(BaseModel):
    event_id: str
    timestamp: str
    node_id: str
    event_type: str
    severity: str
    risk_score: int
    confidence: int
    payload: str
    sync_status: str

class SimulationInjectSchema(BaseModel):
    scenario: str # disaster_detection, sensor_spoofing, internet_failure, complete_network_loss, restoration, reset_normal
    target_node: Optional[str] = "NODE-03"
    override_stage: Optional[float] = None
