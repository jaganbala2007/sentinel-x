"""
Sentinel-X Hazards: Thermal & Extreme Heat Hazards
==================================================
Evaluates:
  - 3-phase AC induction motor winding temperature (PT100 RTD)
  - Gearbox bulk oil temperature
  - Ambient environmental thermal stress
"""

from pydantic import BaseModel

class HeatHazardAssessment(BaseModel):
    hazard_name: str = "Motor Thermal Runaway"
    severity_level: str = "NORMAL"
    risk_score: float = 0.0
    temperature_c: float = 68.5
    rate_of_rise_c_min: float = 0.0
    diagnosis: str = "Operating within Class F insulation limits (< 105°C rise)"
    recommended_action: str = "Nominal ventilation active"

class HeatHazardModule:
    def evaluate(self, motor_temp: float, rate_of_rise: float = 0.0) -> HeatHazardAssessment:
        if motor_temp >= 95.0 or rate_of_rise > 8.0:
            severity = "CRITICAL"
            risk = min(100.0, 80.0 + (motor_temp - 95.0) * 1.5)
            diagnosis = "CRITICAL: Motor stator winding insulation breakdown imminent. Thermal runaway detected."
            action = "De-energize main drive contactor and engage forced cooling fans."
        elif motor_temp >= 80.0 or rate_of_rise > 4.0:
            severity = "WARNING"
            risk = 55.0 + (motor_temp - 80.0) * 1.2
            diagnosis = "WARNING: Temperature exceeds continuous service rating. High winding resistance."
            action = "Reduce belt material load and derate drive frequency."
        elif motor_temp >= 72.0:
            severity = "WATCH"
            risk = 32.0
            diagnosis = "WATCH: Elevated motor operating temperature."
            action = "Inspect motor cooling fan cowling for iron ore dust clogs."
        else:
            severity = "NORMAL"
            risk = 12.0
            diagnosis = "Operating within Class F insulation limits"
            action = "Nominal ventilation active"

        return HeatHazardAssessment(
            severity_level=severity,
            risk_score=round(risk, 1),
            temperature_c=motor_temp,
            rate_of_rise_c_min=round(rate_of_rise, 2),
            diagnosis=diagnosis,
            recommended_action=action
        )

heat_hazard_module = HeatHazardModule()
