"""
Sentinel-X Core: Sensor Abstraction Layer
=========================================
Environment-agnostic abstraction for physical, simulated, and inferred sensor streams.
Enforces strict provenance labeling:
  - LIVE (physically wired & verified)
  - SIMULATED
  - INFERRED
  - OFFLINE
  - PLANNED
"""

import time
import hashlib
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class SensorDataSource(str, Enum):
    LIVE = "LIVE"
    SIMULATED = "SIMULATED"
    INFERRED = "INFERRED"
    OFFLINE = "OFFLINE"
    PLANNED = "PLANNED"

class SensorTrustStatus(str, Enum):
    VERIFIED = "VERIFIED"
    TRUSTED = "TRUSTED"
    SUSPICIOUS = "SUSPICIOUS"
    DEGRADED = "DEGRADED"
    QUARANTINED = "QUARANTINED"

class SensorReading(BaseModel):
    sensor_id: str
    node_id: str = "ESP32-NODE-01"
    parameter: str
    value: float
    unit: str
    timestamp: float = Field(default_factory=time.time)
    data_source: SensorDataSource = SensorDataSource.SIMULATED
    trust_score: float = Field(default=98.0, ge=0.0, le=100.0)
    trust_status: SensorTrustStatus = SensorTrustStatus.TRUSTED
    voting_weight: float = Field(default=1.0, ge=0.0, le=1.0)
    min_physical_limit: Optional[float] = None
    max_physical_limit: Optional[float] = None
    rate_of_change_max: Optional[float] = None
    raw_checksum: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def calculate_checksum(self) -> str:
        payload = f"{self.sensor_id}:{self.parameter}:{self.value}:{self.timestamp}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def is_physically_plausible(self) -> bool:
        if self.min_physical_limit is not None and self.value < self.min_physical_limit:
            return False
        if self.max_physical_limit is not None and self.value > self.max_physical_limit:
            return False
        return True

class SensorRegistry:
    def __init__(self):
        self._sensors: Dict[str, SensorReading] = {}

    def register(self, reading: SensorReading):
        self._sensors[reading.sensor_id] = reading

    def get(self, sensor_id: str) -> Optional[SensorReading]:
        return self._sensors.get(sensor_id)

    def get_all(self) -> List[SensorReading]:
        return list(self._sensors.values())

    def update_trust(self, sensor_id: str, trust_score: float, status: SensorTrustStatus):
        if sensor_id in self._sensors:
            self._sensors[sensor_id].trust_score = trust_score
            self._sensors[sensor_id].trust_status = status
            # Quarantined sensors lose voting authority
            if status == SensorTrustStatus.QUARANTINED:
                self._sensors[sensor_id].voting_weight = 0.0
            elif status == SensorTrustStatus.DEGRADED:
                self._sensors[sensor_id].voting_weight = 0.4
            elif status == SensorTrustStatus.SUSPICIOUS:
                self._sensors[sensor_id].voting_weight = 0.6
            else:
                self._sensors[sensor_id].voting_weight = 1.0

sensor_registry = SensorRegistry()
SensorAbstractionLayer = SensorRegistry
sensor_abstraction_layer = sensor_registry
