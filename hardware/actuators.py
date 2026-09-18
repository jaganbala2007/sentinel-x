"""
Sentinel-X Hardware Abstraction: Local Actuators & Alarms
=========================================================
Controls physical and simulated plant interlocks:
  - Emergency Stop trip relay
  - Conveyor Motor power interlock
  - Industrial 3-stage warning beacon (Green / Yellow / Red)
  - Acoustic safety siren (0 - 110 dB)
  - Emergency ventilation fans
"""

from typing import Dict, Any
from pydantic import BaseModel, Field

class ActuatorState(BaseModel):
    conveyor_motor_relay: bool = Field(default=True, description="True = Motor energized, False = Power cut interlock")
    e_stop_tripped: bool = Field(default=False, description="Emergency stop circuit state")
    warning_beacon_color: str = Field(default="GREEN", description="'GREEN', 'YELLOW', or 'RED'")
    warning_beacon_flashing: bool = Field(default=False, description="Strobe flashing state")
    siren_active: bool = Field(default=False, description="Acoustic horn state")
    siren_db: int = Field(default=0, description="Sound pressure in decibels")
    exhaust_fan_relay: bool = Field(default=False, description="Smoke/gas ventilation relay")
    last_actuation_reason: str = Field(default="System Nominal", description="Reason for state change")
    local_hardware_interlock_active: bool = Field(default=True, description="Enforced on RPi5 without cloud")

class ActuatorManager:
    def __init__(self):
        self.state = ActuatorState()

    def set_nominal(self):
        self.state.conveyor_motor_relay = True
        self.state.e_stop_tripped = False
        self.state.warning_beacon_color = "GREEN"
        self.state.warning_beacon_flashing = False
        self.state.siren_active = False
        self.state.siren_db = 0
        self.state.exhaust_fan_relay = False
        self.state.last_actuation_reason = "System Baseline Nominal"

    def trigger_warning(self, reason: str):
        self.state.warning_beacon_color = "YELLOW"
        self.state.warning_beacon_flashing = True
        self.state.last_actuation_reason = reason

    def trigger_emergency_interlock(self, reason: str):
        """Immediately de-energizes motor and trips red strobe & siren."""
        self.state.conveyor_motor_relay = False
        self.state.e_stop_tripped = True
        self.state.warning_beacon_color = "RED"
        self.state.warning_beacon_flashing = True
        self.state.siren_active = True
        self.state.siren_db = 95
        self.state.last_actuation_reason = reason

    def get_state(self) -> ActuatorState:
        return self.state

actuator_manager = ActuatorManager()
