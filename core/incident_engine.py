"""
Sentinel-X Incident Reconstruction & Timeline Engine
====================================================
Captures chronological state history across physical, cyber, worker, and decision
domains. Provides explainable incident reconstruction, root-cause causal chains,
and comparison across Pre-Incident, During-Incident, and Post-Response states.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class IncidentEvent(BaseModel):
    timestamp_offset_s: int
    time_str: str
    subsystem: str  # MACHINE, SENSOR, CYBER, WORKER, DECISION, EDGE
    event_type: str
    severity: str
    description: str
    telemetry_snapshot: Dict[str, Any]


class IncidentTimeline(BaseModel):
    incident_id: str
    title: str
    target_machine: str
    target_zone: str
    status: str  # RESOLVED, INVESTIGATING, ACTIVE
    events: List[IncidentEvent]
    probable_root_cause_chain: List[str]
    root_cause_confidence: float
    state_comparison: Dict[str, Any]


class IncidentReconstructionEngine:
    def __init__(self):
        pass

    def get_hero_incident_reconstruction(self) -> Dict[str, Any]:
        """
        Returns full reconstruction for the Hero Incident:
        Bearing degradation -> Thermal anomaly -> PLC false telemetry spoofing ->
        Cross-sensor conflict -> Worker exposure -> Automated edge lockout.
        """
        now = datetime.utcnow()
        t0 = now - timedelta(seconds=60)

        events = [
            IncidentEvent(
                timestamp_offset_s=0,
                time_str="10:31:02 UTC",
                subsystem="MACHINE",
                event_type="BEARING_VIBRATION_SPIKE",
                severity="WARNING",
                description="Compressor M-007 shaft vibration harmonics increased from 2.1 mm/s to 8.4 mm/s.",
                telemetry_snapshot={"vibration_mm_s": 8.4, "current_a": 48.5, "rpm": 2980}
            ),
            IncidentEvent(
                timestamp_offset_s=4,
                time_str="10:31:06 UTC",
                subsystem="SENSOR",
                event_type="THERMAL_GRADIENT_DETECTED",
                severity="WARNING",
                description="Independent Thermal Camera 01 detected rapid temperature elevation to 81.4°C.",
                telemetry_snapshot={"thermal_cam_c": 81.4, "aux_rtd_c": 80.8}
            ),
            IncidentEvent(
                timestamp_offset_s=7,
                time_str="10:31:09 UTC",
                subsystem="CYBER",
                event_type="PLC_DATA_MANIPULATION_DETECTED",
                severity="CRITICAL",
                description="PLC_TEMP_M007 reported false low 42.0°C. Cross-sensor validator detected 39.4°C conflict. Trust degraded 94% -> 37%.",
                telemetry_snapshot={"plc_temp_c": 42.0, "true_estimated_temp_c": 81.2, "plc_trust": 37.0}
            ),
            IncidentEvent(
                timestamp_offset_s=9,
                time_str="10:31:11 UTC",
                subsystem="WORKER",
                event_type="UNAUTHORIZED_WORKER_PROXIMITY",
                severity="HIGH",
                description="Worker WRK-014 entered Zone-B in dangerous proximity (1.1m) to overheating Machine M-007.",
                telemetry_snapshot={"worker_id": "WRK-014", "zone": "Zone-B", "distance_m": 1.1, "safety_score": 58.0}
            ),
            IncidentEvent(
                timestamp_offset_s=11,
                time_str="10:31:13 UTC",
                subsystem="DECISION",
                event_type="AUTOMATED_EMERGENCY_DECISION",
                severity="CRITICAL",
                description="Decision Engine issued sub-100ms emergency valve lockout and Zone-B audio-visual evacuation.",
                telemetry_snapshot={"decision": "RESTRICT_ZONE_AND_OVERRIDE_M007", "confidence": 0.96}
            ),
            IncidentEvent(
                timestamp_offset_s=12,
                time_str="10:31:14 UTC",
                subsystem="EDGE",
                event_type="SUB_100MS_OVERRIDE_EXECUTED",
                severity="INFO",
                description="ESP32 / Modbus edge controller executed machine override in 42.8 ms.",
                telemetry_snapshot={"measured_latency_ms": 42.8, "status": "LOCKED_OUT"}
            )
        ]

        causal_chain = [
            "1. Mechanical Bearing Wear (Overdue Maintenance on M-007)",
            "2. Severe Vibration (8.4 mm/s) inducing thermal frictional runaway",
            "3. Internal Bearing Temperature elevated rapidly to ~82.0°C",
            "4. Unauthorized PLC Modbus telemetry spoofing masked overheating by reporting 42.0°C",
            "5. Sentinel-X Cross-Sensor Consensus detected conflict with Thermal Imager (81.4°C) and degraded PLC trust to 37%",
            "6. Worker WRK-014 intruded into Zone-B during uncontained hazard",
            "7. Sentinel-X AI Decision Engine executed autonomous emergency lockout in 42.8ms."
        ]

        state_comparison = {
            "pre_incident": {
                "label": "T-60s (Nominal State)",
                "machine_health": 88.0,
                "plc_temperature_c": 70.2,
                "thermal_camera_c": 70.4,
                "plc_trust_score": 94.0,
                "worker_safety_score": 95.0,
                "global_risk": "SAFE"
            },
            "during_incident": {
                "label": "T+7s (Integrity Attack & Hazard State)",
                "machine_health": 38.0,
                "plc_temperature_c": 42.0,
                "thermal_camera_c": 81.4,
                "plc_trust_score": 37.0,
                "worker_safety_score": 58.0,
                "global_risk": "CRITICAL"
            },
            "post_response": {
                "label": "T+15s (Safe Overridden State)",
                "machine_health": 45.0,
                "plc_temperature_c": 42.0,
                "thermal_camera_c": 64.0,
                "plc_trust_score": 37.0,
                "worker_safety_score": 92.0,
                "global_risk": "MEDIUM"
            }
        }

        timeline = IncidentTimeline(
            incident_id="INC-2026-0828-001",
            title="Machine M-007 Thermal Runaway with PLC Spoofing & Zone Intrusion",
            target_machine="M-007",
            target_zone="Zone-B",
            status="RESOLVED",
            events=events,
            probable_root_cause_chain=causal_chain,
            root_cause_confidence=0.94,
            state_comparison=state_comparison
        )

        return timeline.model_dump()


incident_reconstruction_engine = IncidentReconstructionEngine()
