"""
Sentinel-X What-If Digital Twin Simulation Sandbox
===================================================
Allows operators to test operational and stress hypotheses (e.g. RPM +15%,
production load increases, cooling efficiency drops, delayed maintenance,
worker movement into hazard zones) without impacting physical machinery.

All outputs are strictly labeled with data_state = SIMULATED.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class WhatIfRequest(BaseModel):
    machine_id: str = "M-007"
    rpm_delta_pct: float = Field(0.0, ge=-50.0, le=100.0, description="RPM change percentage (e.g. +15%)")
    load_delta_pct: float = Field(0.0, ge=-50.0, le=100.0, description="Production load change percentage")
    cooling_efficiency_pct: float = Field(100.0, ge=10.0, le=100.0, description="Cooling system efficiency")
    maintenance_delay_hours: float = Field(0.0, ge=0.0, le=1000.0, description="Hypothetical maintenance delay")
    worker_zone_override: Optional[str] = Field(None, description="Simulated worker location")


class WhatIfEngine:
    def __init__(self):
        pass

    def simulate_scenario(self, req: WhatIfRequest) -> Dict[str, Any]:
        """
        Calculates physics-informed simulated response for given hypothetical operational changes.
        """
        # Baseline M-007 values
        base_temp = 72.0
        base_vib = 3.2
        base_current = 35.0
        base_rul = 120.0
        base_energy_kw = 45.0

        # Simulated changes
        # 1. RPM increase increases vibration non-linearly (vibration ~ RPM^1.5) and temp
        rpm_factor = 1.0 + (req.rpm_delta_pct / 100.0)
        load_factor = 1.0 + (req.load_delta_pct / 100.0)
        cooling_factor = req.cooling_efficiency_pct / 100.0

        pred_temp = base_temp + (req.rpm_delta_pct * 0.55) + (req.load_delta_pct * 0.40) + ((1.0 - cooling_factor) * 28.0)
        pred_vib = base_vib * (rpm_factor ** 1.6) * (load_factor ** 0.8)
        pred_current = base_current * load_factor * (rpm_factor ** 0.9)
        pred_energy_kw = base_energy_kw * (load_factor ** 1.1) * (rpm_factor ** 1.3)

        # RUL degradation acceleration
        rul_acceleration = max(0.5, ((pred_temp / 70.0) ** 2.2) * ((pred_vib / 3.0) ** 1.8))
        pred_rul = max(2.0, (base_rul / rul_acceleration) - (req.maintenance_delay_hours * 0.15))

        # Risk transition
        if pred_temp > 80.0 or pred_vib > 6.5 or pred_rul < 45.0:
            risk_level = "CRITICAL" if pred_temp > 85.0 else "HIGH"
            risk_score = min(98.0, 65.0 + (pred_temp - 75.0) * 1.8 + (pred_vib - 4.0) * 4.0)
        elif pred_temp > 75.0 or pred_vib > 4.5:
            risk_level = "MEDIUM"
            risk_score = 52.0
        else:
            risk_level = "LOW"
            risk_score = 22.0

        # Recommendation synthesis
        if req.rpm_delta_pct > 10.0 and risk_level in ["HIGH", "CRITICAL"]:
            safe_rpm_delta = round(max(3.0, req.rpm_delta_pct * 0.45), 1)
            rec = f"UNSAFE SCENARIO: Operating at +{req.rpm_delta_pct:.0f}% RPM induces severe thermal ({pred_temp:.1f}°C) and vibration ({pred_vib:.1f} mm/s) stress, reducing Bearing RUL by {base_rul - pred_rul:.1f} hours. Recommend capping RPM increase to +{safe_rpm_delta}%."
        elif req.cooling_efficiency_pct < 80.0:
            rec = f"Cooling degradation elevates thermal risks. Ensure auxiliary heat exchangers are engaged before increasing load."
        else:
            rec = "Simulated operational parameters remain within safe structural envelopes."

        return {
            "scenario_name": f"Hypothetical RPM {req.rpm_delta_pct:+.0f}%, Load {req.load_delta_pct:+.0f}% on {req.machine_id}",
            "machine_id": req.machine_id,
            "data_state": "SIMULATED_PREDICTION",
            "inputs": req.model_dump(),
            "baseline": {
                "temperature_c": base_temp,
                "vibration_mm_s": base_vib,
                "motor_current_a": base_current,
                "power_kw": base_energy_kw,
                "estimated_rul_hours": base_rul,
                "risk_level": "LOW"
            },
            "predicted_outcomes": {
                "predicted_temperature_c": round(pred_temp, 1),
                "temperature_delta_c": round(pred_temp - base_temp, 1),
                "predicted_vibration_mm_s": round(pred_vib, 2),
                "vibration_delta_mm_s": round(pred_vib - base_vib, 2),
                "predicted_power_kw": round(pred_energy_kw, 1),
                "energy_delta_pct": round(((pred_energy_kw - base_energy_kw) / base_energy_kw) * 100.0, 1),
                "predicted_rul_hours": round(pred_rul, 1),
                "rul_impact_hours": round(pred_rul - base_rul, 1),
                "predicted_risk_score": round(risk_score, 1),
                "predicted_risk_level": risk_level
            },
            "ai_recommendation": rec,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


what_if_engine = WhatIfEngine()
