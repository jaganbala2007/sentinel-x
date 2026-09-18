"""
Sentinel-X Hazards: Fire, Gas, Power, Flood, and Structural Modules
===================================================================
"""

from pydantic import BaseModel

class FireGasHazardAssessment(BaseModel):
    hazard_name: str
    severity_level: str
    risk_score: float
    reading: float
    unit: str
    diagnosis: str
    action: str

class FireGasHazardModule:
    def evaluate_fire(self, smoke_ppm: float, temp_c: float) -> FireGasHazardAssessment:
        if smoke_ppm >= 150.0 or temp_c >= 90.0:
            return FireGasHazardAssessment(
                hazard_name="Industrial Fire / Cable Combustion",
                severity_level="CRITICAL",
                risk_score=92.0,
                reading=smoke_ppm,
                unit="ppm",
                diagnosis="Dense ionization smoke detected in drive bay.",
                action="Activate automated dry-chemical suppression & exhaust fans."
            )
        elif smoke_ppm >= 60.0:
            return FireGasHazardAssessment(
                hazard_name="Industrial Fire / Cable Combustion",
                severity_level="WARNING",
                risk_score=58.0,
                reading=smoke_ppm,
                unit="ppm",
                diagnosis="Elevated hydrocarbon / insulation outgassing detected.",
                action="Flash yellow beacon and alert electrical maintenance team."
            )
        return FireGasHazardAssessment(
            hazard_name="Industrial Fire / Cable Combustion",
            severity_level="NORMAL",
            risk_score=5.0,
            reading=smoke_ppm,
            unit="ppm",
            diagnosis="Atmosphere within safe occupational limits.",
            action="Continuous monitoring active."
        )

    def evaluate_gas(self, gas_ppm: float) -> FireGasHazardAssessment:
        if gas_ppm >= 200.0:
            return FireGasHazardAssessment(
                hazard_name="Toxic / Combustible Gas Leak",
                severity_level="CRITICAL",
                risk_score=90.0,
                reading=gas_ppm,
                unit="ppm",
                diagnosis="LEL threshold exceeded for toxic gas.",
                action="Execute plant area evacuation and cut spark-generating equipment."
            )
        return FireGasHazardAssessment(
            hazard_name="Toxic / Combustible Gas Leak",
            severity_level="NORMAL",
            risk_score=4.0,
            reading=gas_ppm,
            unit="ppm",
            diagnosis="Air quality nominal.",
            action="Baseline ventilation active."
        )

fire_gas_hazard_module = FireGasHazardModule()

class FloodHazardModule:
    def evaluate_flood(self, water_level_m: float, rainfall_mm_hr: float) -> FireGasHazardAssessment:
        if water_level_m >= 12.0 or rainfall_mm_hr >= 100.0:
            return FireGasHazardAssessment(
                hazard_name="River Basin Flash Flood",
                severity_level="CRITICAL",
                risk_score=94.0,
                reading=water_level_m,
                unit="meters",
                diagnosis="Water level exceeds HFL (Highest Flood Level). Inundation underway.",
                action="Trigger river acoustic warning horns and alert state NDRF EOC."
            )
        elif water_level_m >= 8.0:
            return FireGasHazardAssessment(
                hazard_name="River Basin Flash Flood",
                severity_level="WARNING",
                risk_score=62.0,
                reading=water_level_m,
                unit="meters",
                diagnosis="Water level above Danger Level.",
                action="Prepare downstream barrage gates and dispatch evacuation team."
            )
        return FireGasHazardAssessment(
            hazard_name="River Basin Flash Flood",
            severity_level="NORMAL",
            risk_score=8.0,
            reading=water_level_m,
            unit="meters",
            diagnosis="River stage within safe hydraulic design capacity.",
            action="Maintain automated gauge polling."
        )

flood_hazard_module = FloodHazardModule()
