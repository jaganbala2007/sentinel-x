"""
Sentinel-X Core: Autonomous Response Engine
===========================================
Executes deterministic, edge-first safety decisions directly on Raspberry Pi 5.
Interlocks with physical actuators, relays, strobes, and acoustic alarms.
CRITICAL SAFETY LAW:
Never depends on Internet, cloud, LLM, remote API, or satellite connectivity.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time

class ResponseActionType(str, Enum):
    NOMINAL = "NOMINAL"
    MAINTENANCE_ADVISORY = "MAINTENANCE_ADVISORY"
    WARNING_BEACON = "WARNING_BEACON"
    SPEED_DERATE = "SPEED_DERATE"
    EMERGENCY_STOP = "EMERGENCY_STOP"
    EVACUATION_ALARM = "EVACUATION_ALARM"
    VENTILATION_ENGAGE = "VENTILATION_ENGAGE"

class SafetyAction(BaseModel):
    action_type: ResponseActionType
    target: str # e.g. "CONVEYOR_MOTOR_RELAY", "WARNING_BEACON", "SIREN_110DB"
    state: Any # True/False, "RED", 95, etc.
    priority: str # LOW, MEDIUM, HIGH, CRITICAL
    reason: str
    autonomous_decision: bool = True
    executed_at: float = Field(default_factory=time.time)

class AutonomousResponseEngine:
    def __init__(self):
        self.action_history: List[SafetyAction] = []

    def evaluate_response(self, risk_level: str, hazard_type: str, details: Dict[str, Any]) -> List[SafetyAction]:
        """
        Determines and fires local autonomous interlocks based on risk severity.
        """
        actions: List[SafetyAction] = []

        if risk_level == "CRITICAL":
            # 1. Immediate hardware cut
            actions.append(SafetyAction(
                action_type=ResponseActionType.EMERGENCY_STOP,
                target="CONVEYOR_MOTOR_RELAY",
                state=False, # de-energize
                priority="CRITICAL",
                reason=f"Immediate E-Stop trip triggered by {hazard_type} critical severity"
            ))
            # 2. Visual Strobe Red
            actions.append(SafetyAction(
                action_type=ResponseActionType.WARNING_BEACON,
                target="WARNING_BEACON",
                state="RED",
                priority="CRITICAL",
                reason=f"Visual red strobe for {hazard_type}"
            ))
            # 3. Acoustic Siren
            actions.append(SafetyAction(
                action_type=ResponseActionType.EVACUATION_ALARM,
                target="SIREN_110DB",
                state=95, # dB
                priority="CRITICAL",
                reason="Audible 95dB industrial alarm initiated locally"
            ))
            # 4. If gas or smoke, engage ventilation
            if "gas" in hazard_type.lower() or "smoke" in hazard_type.lower() or "fire" in hazard_type.lower():
                actions.append(SafetyAction(
                    action_type=ResponseActionType.VENTILATION_ENGAGE,
                    target="EXHAUST_FAN_RELAY",
                    state=True,
                    priority="HIGH",
                    reason="Smoke/Gas exhaust extraction activated"
                ))

        elif risk_level == "WARNING":
            actions.append(SafetyAction(
                action_type=ResponseActionType.WARNING_BEACON,
                target="WARNING_BEACON",
                state="YELLOW",
                priority="MEDIUM",
                reason=f"Warning threshold exceeded for {hazard_type}"
            ))
            actions.append(SafetyAction(
                action_type=ResponseActionType.SPEED_DERATE,
                target="CONVEYOR_VFD_SPEED",
                state=50, # derate to 50%
                priority="MEDIUM",
                reason=f"Speed derated to 50% to prevent thermal/mechanical run-away"
            ))

        elif risk_level == "WATCH":
            actions.append(SafetyAction(
                action_type=ResponseActionType.MAINTENANCE_ADVISORY,
                target="OPERATOR_PANEL",
                state="FLAG_WATCH",
                priority="LOW",
                reason=f"Elevated metrics observed in {hazard_type}. Scheduled check advised."
            ))

        else: # NORMAL
            actions.append(SafetyAction(
                action_type=ResponseActionType.NOMINAL,
                target="WARNING_BEACON",
                state="GREEN",
                priority="LOW",
                reason="System nominal baseline"
            ))

        self.action_history.extend(actions)
        return actions

response_engine = AutonomousResponseEngine()
SafetyResponseEngine = AutonomousResponseEngine
ResponseEngine = AutonomousResponseEngine
