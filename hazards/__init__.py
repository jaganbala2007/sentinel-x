"""
Sentinel-X Hazards Package
===========================
Modular hazard evaluators:
  - equipment: Bearing degradation, roller wear, mechanical failure
  - heat: Motor winding thermal runaway, extreme heat
  - worker_safety: Pinch-point intrusion, human-machine conflict, E-Stop trip
  - fire: Smoke combustion, electrical insulation fire
  - gas: Hazardous / toxic gas leaks
  - flood: Hydrological flash flood, rate of water rise
"""

from typing import Dict, Any, List
from hazards.equipment import equipment_hazard_module, EquipmentHazardAssessment
from hazards.heat import heat_hazard_module, HeatHazardAssessment
from hazards.worker_safety import worker_safety_hazard_module, WorkerHazardAssessment
from hazards.fire import fire_gas_hazard_module, flood_hazard_module, FireGasHazardAssessment

class HazardEngine:
    def __init__(self):
        pass

    def evaluate_all(self, telemetry: Dict[str, float]) -> Dict[str, Any]:
        """Evaluates industrial and environmental hazards from live/simulated telemetry."""
        motor_temp = telemetry.get("motor_temperature", 68.5)
        vibration = telemetry.get("bearing_vibration", 2.4)
        gearbox_temp = telemetry.get("gearbox_temperature", 62.0)
        belt_speed = telemetry.get("belt_speed", 2.2)
        worker_prox = telemetry.get("worker_proximity", 4.5)
        estop = bool(telemetry.get("estop_state", 0.0))
        smoke = telemetry.get("smoke_gas_ppm", 18.0)
        water_lvl = telemetry.get("water_level", 4.8)

        eq_eval = equipment_hazard_module.evaluate(vibration, motor_temp, gearbox_temp, belt_speed)
        ht_eval = heat_hazard_module.evaluate(motor_temp)
        wk_eval = worker_safety_hazard_module.evaluate(worker_prox, belt_speed, estop)
        fr_eval = fire_gas_hazard_module.evaluate_fire(smoke, motor_temp)
        fl_eval = flood_hazard_module.evaluate_flood(water_lvl, 10.0)

        all_hazards = [
            {"name": eq_eval.hazard_name, "severity": eq_eval.severity_level, "risk": eq_eval.risk_score, "diagnosis": eq_eval.diagnosis, "action": eq_eval.recommended_action},
            {"name": ht_eval.hazard_name, "severity": ht_eval.severity_level, "risk": ht_eval.risk_score, "diagnosis": ht_eval.diagnosis, "action": ht_eval.recommended_action},
            {"name": wk_eval.hazard_name, "severity": wk_eval.severity_level, "risk": wk_eval.risk_score, "diagnosis": wk_eval.diagnosis, "action": wk_eval.recommended_action},
            {"name": fr_eval.hazard_name, "severity": fr_eval.severity_level, "risk": fr_eval.risk_score, "diagnosis": fr_eval.diagnosis, "action": fr_eval.action},
        ]

        # Determine highest severity
        severities = [h["severity"] for h in all_hazards]
        if "CRITICAL" in severities:
            peak_severity = "CRITICAL"
        elif "WARNING" in severities:
            peak_severity = "WARNING"
        elif "WATCH" in severities:
            peak_severity = "WATCH"
        else:
            peak_severity = "NORMAL"

        peak_risk = max(h["risk"] for h in all_hazards)

        return {
            "overall_severity": peak_severity,
            "overall_risk": peak_risk,
            "hazards": all_hazards,
            "active_threat_count": sum(1 for h in all_hazards if h["severity"] != "NORMAL")
        }

hazard_engine = HazardEngine()

__all__ = [
    "equipment_hazard_module",
    "EquipmentHazardAssessment",
    "heat_hazard_module",
    "HeatHazardAssessment",
    "worker_safety_hazard_module",
    "WorkerHazardAssessment",
    "fire_gas_hazard_module",
    "flood_hazard_module",
    "FireGasHazardAssessment",
    "hazard_engine",
]
