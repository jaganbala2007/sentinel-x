"""
Sentinel-X Hardware Abstraction: Power Resilience Manager
==========================================================
Monitors edge battery capacity, rail input voltage, system load,
and solar harvesting. Supports continuous autonomous safety during
grid blackouts or remote alpine deployment.

States:
  NORMAL   - Grid mains active, battery >= 30%
  LOW      - Battery 15-30%, non-essential telemetry throttled
  CRITICAL - Battery < 15%, emergency interlock reserved power
  BACKUP   - Grid mains loss, running on secondary battery bank
"""

import time
from typing import Dict, Any
from pydantic import BaseModel, Field

class PowerMetrics(BaseModel):
    battery_pct: float = Field(default=96.4, description="Battery state of charge (0-100%)")
    input_voltage: float = Field(default=24.2, description="Main bus / rail voltage in Volts")
    load_watts: float = Field(default=18.5, description="Edge computing & sensing load in Watts")
    solar_input_watts: float = Field(default=45.0, description="Solar harvester input in Watts")
    estimated_runtime_hours: float = Field(default=38.4, description="Estimated battery autonomy runtime in hours")
    power_state: str = Field(default="NORMAL", description="NORMAL | LOW | CRITICAL | BACKUP")
    mains_present: bool = Field(default=True, description="Whether grid mains power is active")
    last_update: str = Field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

class PowerManager:
    def __init__(self):
        self.metrics = PowerMetrics()

    def get_status(self) -> PowerMetrics:
        return self.metrics

    def update_power_state(self, battery_pct: float, mains_present: bool = True, solar_watts: float = 0.0) -> PowerMetrics:
        self.metrics.battery_pct = max(0.0, min(100.0, battery_pct))
        self.metrics.mains_present = mains_present
        self.metrics.solar_input_watts = solar_watts
        
        if not mains_present:
            self.metrics.power_state = "BACKUP"
            self.metrics.input_voltage = 23.4
        elif self.metrics.battery_pct < 15.0:
            self.metrics.power_state = "CRITICAL"
        elif self.metrics.battery_pct < 30.0:
            self.metrics.power_state = "LOW"
        else:
            self.metrics.power_state = "NORMAL"

        # Calculate estimated runtime based on 500Wh battery bank
        battery_energy_wh = 500.0 * (self.metrics.battery_pct / 100.0)
        net_load = max(1.0, self.metrics.load_watts - (solar_watts * 0.8 if solar_watts > 0 else 0))
        self.metrics.estimated_runtime_hours = round(battery_energy_wh / net_load, 1)
        self.metrics.last_update = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return self.metrics

power_manager = PowerManager()
