"""
Sentinel-X Environments Package
================================
Environment profiles:
  - industrial: Flagship Industrial Manufacturing / Conveyor Plant
  - indoor: Facilities, Warehouses, Hospitals, Data Centers
  - natural: River Flood, Catchment, Landslides
  - urban: Underpasses, Drainage, Roads
  - infrastructure: Dams, Bridges, Tunnels
  - remote: Off-grid, Cold Climate, Extreme Environments
  - custom: Dynamic User Configuration
"""

from typing import Dict, List, Optional
from environments.base import EnvironmentProfile, SensorSpec, HazardRule
from environments.industrial import industrial_profile
from environments.indoor import indoor_profile
from environments.natural import natural_profile
from environments.urban import urban_profile, infrastructure_profile, remote_profile, custom_profile

class EnvironmentRegistry:
    def __init__(self):
        self._profiles: Dict[str, EnvironmentProfile] = {
            "INDUSTRIAL": industrial_profile,
            "INDOOR": indoor_profile,
            "NATURAL": natural_profile,
            "URBAN": urban_profile,
            "INFRASTRUCTURE": infrastructure_profile,
            "REMOTE": remote_profile,
            "CUSTOM": custom_profile,
        }
        self.active_type: str = "INDUSTRIAL"

    def get_active_profile(self) -> EnvironmentProfile:
        return self._profiles.get(self.active_type, industrial_profile)

    def set_active_profile(self, env_type: str) -> bool:
        env_upper = env_type.upper()
        if env_upper in self._profiles:
            self.active_type = env_upper
            return True
        return False

    def list_profiles(self) -> List[Dict[str, str]]:
        return [
            {"id": p.id, "name": p.name, "type": p.type, "location": p.location, "digital_twin_type": p.digital_twin_type}
            for p in self._profiles.values()
        ]

environment_registry = EnvironmentRegistry()

__all__ = [
    "EnvironmentProfile",
    "SensorSpec",
    "HazardRule",
    "industrial_profile",
    "indoor_profile",
    "natural_profile",
    "urban_profile",
    "infrastructure_profile",
    "remote_profile",
    "custom_profile",
    "environment_registry",
]
