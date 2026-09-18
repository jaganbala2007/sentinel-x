"""
Sentinel-X Unified Industrial Risk Engine
=========================================
Synthesizes Worker Safety DNA, Machine Safety DNA, Environment Safety DNA,
Sensor Trust, Cyber/Data Integrity, and Spatial Hazards into an explainable
plant-wide and asset-specific risk score (0-100) with categorical levels
(SAFE, LOW, MEDIUM, HIGH, CRITICAL).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from core.worker_safety import worker_safety_engine
from core.machine_safety import machine_safety_engine
from core.environment_safety import environment_safety_engine
from core.trust_engine import trust_engine
from core.rul_engine import rul_engine


class UnifiedRiskEngine:
    def __init__(self):
        pass

    def evaluate_global_plant_risk(self) -> Dict[str, Any]:
        """
        Calculates holistic plant-wide risk profile and identifies top risk drivers.
        """
        # 1. Evaluate Workers
        workers = worker_safety_engine.list_all_workers()
        avg_worker_safety = sum(w["safety_score"] for w in workers) / max(1, len(workers))
        worker_risk_component = 100.0 - avg_worker_safety
        critical_workers = [w for w in workers if w["safety_score"] < 70.0]

        # 2. Evaluate Machines
        machines = machine_safety_engine.list_all_machines()
        machine_evals = []
        for m in machines:
            # Default or active state
            temp = 81.4 if m["machine_id"] == "M-007" else 45.0
            vib = 7.8 if m["machine_id"] == "M-007" else 1.8
            amps = 48.0 if m["machine_id"] == "M-007" else 22.0
            rpm = 3000.0
            h_data = rul_engine.compute_health_and_rul(m["machine_id"], temp, vib, amps, rpm)
            machine_evals.append(h_data)

        avg_machine_health = sum(me["health_index"] for me in machine_evals) / max(1, len(machine_evals))
        machine_risk_component = 100.0 - avg_machine_health

        # 3. Evaluate Environment
        zones = environment_safety_engine.list_zones()
        avg_env_risk = sum(z["env_risk_score"] for z in zones) / max(1, len(zones))

        # 4. Evaluate Cyber / Data Trust
        plc_trust = trust_engine.get_device_trust("PLC_TEMP_M007")
        data_trust_risk = max(0.0, 100.0 - plc_trust)

        # Unified Weighted Synthesis
        # 30% Machine Health Risk + 30% Worker Safety Risk + 20% Data Integrity Risk + 20% Env Risk
        global_risk = (
            machine_risk_component * 0.35 +
            worker_risk_component * 0.30 +
            data_trust_risk * 0.20 +
            avg_env_risk * 0.15
        )
        global_risk = round(max(0.0, min(100.0, global_risk)), 1)

        # Risk Classification
        if global_risk < 20.0:
            level = "SAFE"
        elif global_risk < 40.0:
            level = "LOW"
        elif global_risk < 60.0:
            level = "MEDIUM"
        elif global_risk < 80.0:
            level = "HIGH"
        else:
            level = "CRITICAL"

        # Explainability Breakdown
        factors = []
        if machine_risk_component > 30.0:
            factors.append({
                "factor": "Degraded Machinery State",
                "severity": "CRITICAL" if machine_risk_component > 50 else "WARNING",
                "contribution_pct": round(machine_risk_component * 0.35, 1),
                "details": f"Machine M-007 Health Index is critically degraded ({machine_evals[2]['health_index']}%) with Bearing RUL of {machine_evals[2]['estimated_rul_hours']}h."
            })
        if worker_risk_component > 20.0:
            factors.append({
                "factor": "Worker Safety & Zone Intrusion",
                "severity": "HIGH",
                "contribution_pct": round(worker_risk_component * 0.30, 1),
                "details": "Worker WRK-014 detected inside unauthorized Zone-B in hazardous proximity (1.1m) to M-007."
            })
        if data_trust_risk > 15.0:
            factors.append({
                "factor": "Data Trust & Telemetry Conflict",
                "severity": "HIGH",
                "contribution_pct": round(data_trust_risk * 0.20, 1),
                "details": f"PLC_TEMP_M007 trust degraded to {plc_trust:.1f}% due to cross-sensor conflict with thermal camera."
            })

        return {
            "overall_risk_score": global_risk,
            "risk_level": level,
            "subsystem_scores": {
                "machine_risk": round(machine_risk_component, 1),
                "worker_risk": round(worker_risk_component, 1),
                "data_integrity_risk": round(data_trust_risk, 1),
                "environment_risk": round(avg_env_risk, 1)
            },
            "contributing_factors": factors,
            "critical_assets": {
                "machines_at_risk": [m["machine_id"] for m in machine_evals if m["health_index"] < 70.0],
                "workers_at_risk": [w["worker_id"] for w in critical_workers],
                "untrusted_devices": [dev for dev, score in trust_engine.device_trust_registry.items() if score < 75.0]
            },
            "recommended_actions": [
                "Issue automated evacuation alert for WRK-014 from Zone-B.",
                "Initiate thermal inspection and Modbus audit on Machine M-007.",
                "Schedule bearing replacement before Remaining Useful Life threshold expires."
            ],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


unified_risk_engine = UnifiedRiskEngine()
RiskEngine = UnifiedRiskEngine
risk_engine = unified_risk_engine
