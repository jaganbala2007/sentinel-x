"""
Sentinel-X Environment Safety DNA Subsystem
===========================================
Tracks multi-zone environmental telemetry (ambient temperature, humidity,
toxic gas ppm, ambient noise dB, lighting lux, occupancy, and emergency states).
"""

from typing import Dict, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ZoneEnvironmentDNA(BaseModel):
    zone_id: str
    name: str
    ambient_temp_c: float
    relative_humidity_pct: float
    co2_ppm: float
    voc_ppb: float
    noise_db: float
    occupancy_count: int
    emergency_lockout_active: bool = False
    air_quality_index: str = "GOOD"
    env_risk_score: float = 10.0


class EnvironmentSafetyEngine:
    def __init__(self):
        self.zones: Dict[str, ZoneEnvironmentDNA] = {
            "Zone-A": ZoneEnvironmentDNA(
                zone_id="Zone-A",
                name="Main Fabrication & Stamping Bay",
                ambient_temp_c=24.5,
                relative_humidity_pct=45.0,
                co2_ppm=420.0,
                voc_ppb=85.0,
                noise_db=72.0,
                occupancy_count=4,
                env_risk_score=12.0
            ),
            "Zone-B": ZoneEnvironmentDNA(
                zone_id="Zone-B",
                name="High-Pressure Rotary Compressor Cell",
                ambient_temp_c=31.8,
                relative_humidity_pct=38.0,
                co2_ppm=510.0,
                voc_ppb=180.0,
                noise_db=84.5,
                occupancy_count=1,
                env_risk_score=48.0
            ),
            "Zone-C": ZoneEnvironmentDNA(
                zone_id="Zone-C",
                name="Automated Logistics & Conveyor Corridor",
                ambient_temp_c=22.0,
                relative_humidity_pct=50.0,
                co2_ppm=390.0,
                voc_ppb=60.0,
                noise_db=68.0,
                occupancy_count=2,
                env_risk_score=8.0
            ),
            "Zone-D": ZoneEnvironmentDNA(
                zone_id="Zone-D",
                name="Chemical & Lubrication Pumping Array",
                ambient_temp_c=26.0,
                relative_humidity_pct=42.0,
                co2_ppm=460.0,
                voc_ppb=110.0,
                noise_db=76.0,
                occupancy_count=0,
                env_risk_score=22.0
            ),
        }

    def get_zone(self, zone_id: str) -> Dict[str, Any]:
        if zone_id in self.zones:
            return self.zones[zone_id].model_dump()
        return {}

    def list_zones(self) -> List[Dict[str, Any]]:
        return [z.model_dump() for z in self.zones.values()]

    def update_zone_telemetry(self, zone_id: str, updates: Dict[str, Any]) -> ZoneEnvironmentDNA:
        if zone_id not in self.zones:
            raise KeyError(f"Zone {zone_id} not recognized.")
        z = self.zones[zone_id]
        for k, v in updates.items():
            if hasattr(z, k):
                setattr(z, k, v)
        # Recalculate environment risk score
        risk = 5.0
        if z.ambient_temp_c > 35.0:
            risk += 25.0
        if z.noise_db > 85.0:
            risk += 20.0
        if z.co2_ppm > 1000.0:
            risk += 30.0
        if z.emergency_lockout_active:
            risk += 50.0
        z.env_risk_score = min(100.0, risk)
        return z


environment_safety_engine = EnvironmentSafetyEngine()
