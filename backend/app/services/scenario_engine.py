"""
Sentinel-X Deterministic Disaster Scenario Simulator Engine
============================================================
Runs step-by-step disaster simulations for hackathon judging and testing.
Feeds simulated sensor data through the EXACT same risk, correlation, and event
pipelines as live ESP32 hardware telemetry.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List

class ScenarioEngine:
    SCENARIOS = {
        "FIRE_SMOKE": {
            "name": "Fire / Smoke / Air Quality Hazard",
            "zone": "ZONE_B",
            "steps": [
                {"gas": 420, "temp": 32.5, "vib": 0.5, "water": 0.0, "desc": "Baseline Normal Air Quality & Thermal Load"},
                {"gas": 1200, "temp": 36.0, "vib": 0.6, "water": 0.0, "desc": "MQ-135 Gas Anomaly Detected - Rate of Rise Increasing"},
                {"gas": 2400, "temp": 42.8, "vib": 0.8, "water": 0.0, "desc": "Multi-Sensor Cross Validation: High Gas + Thermal Elevation"},
                {"gas": 3100, "temp": 54.2, "vib": 1.1, "water": 0.0, "desc": "CRITICAL FIRE HAZARD BREACH - Evacuation Interlock Triggered"},
                {"gas": 950, "temp": 38.0, "vib": 0.5, "water": 0.0, "desc": "Atmospheric Scrubbing & Response Team Action"},
                {"gas": 420, "temp": 32.9, "vib": 0.5, "water": 0.0, "desc": "Incident Stabilized - Recalibrated Baseline"}
            ]
        },
        "FLOOD_INUNDATION": {
            "name": "Flood / Water-Level Inundation",
            "zone": "ZONE_A",
            "steps": [
                {"gas": 410, "temp": 28.0, "vib": 0.4, "water": 0.1, "desc": "Nominal Hydrological Baseline"},
                {"gas": 410, "temp": 28.1, "vib": 0.4, "water": 0.6, "desc": "Water Level Rising (+0.5m) - Watch Threshold"},
                {"gas": 415, "temp": 27.9, "vib": 0.5, "water": 1.4, "desc": "Hydrological Warning Breach - Inundation Rate >0.08m/min"},
                {"gas": 420, "temp": 27.5, "vib": 0.5, "water": 2.3, "desc": "CRITICAL FLOOD EVENT - Low-Lying Switchgear Isolation Triggered"},
                {"gas": 410, "temp": 28.0, "vib": 0.4, "water": 0.8, "desc": "Sump Pump Deployment & Drainage Progressing"},
                {"gas": 410, "temp": 28.0, "vib": 0.4, "water": 0.1, "desc": "Water Receded - Zone A Cleared"}
            ]
        },
        "EARTHQUAKE_VIBRATION": {
            "name": "Earthquake / Structural Vibration Event",
            "zone": "ZONE_C",
            "steps": [
                {"gas": 400, "temp": 30.0, "vib": 0.5, "water": 0.0, "desc": "Quiet Structural Baseline"},
                {"gas": 400, "temp": 30.1, "vib": 2.2, "water": 0.0, "desc": "ADXL345 Acceleration Spike - Seismic Tremor Warning"},
                {"gas": 405, "temp": 30.2, "vib": 6.8, "water": 0.0, "desc": "CRITICAL STRUCTURAL SEISMIC BREACH - Emergency Assembly Activated"},
                {"gas": 400, "temp": 30.1, "vib": 1.8, "water": 0.0, "desc": "Aftershock Tremors Subsidizing"},
                {"gas": 400, "temp": 30.0, "vib": 0.5, "water": 0.0, "desc": "Structural Integrity Inspection Passed"}
            ]
        },
        "EXTREME_HEAT": {
            "name": "Extreme Heat / Environmental Hazard",
            "zone": "ZONE_A",
            "steps": [
                {"gas": 400, "temp": 32.0, "vib": 0.5, "water": 0.0, "desc": "Nominal Summer Thermal Conditions"},
                {"gas": 410, "temp": 41.5, "vib": 0.5, "water": 0.0, "desc": "Thermal Stress Warning Threshold Exceeded"},
                {"gas": 420, "temp": 49.8, "vib": 0.6, "water": 0.0, "desc": "CRITICAL EXTREME HEAT HAZARD - HVAC Booster Engaged"},
                {"gas": 405, "temp": 35.0, "vib": 0.5, "water": 0.0, "desc": "Cooling Active - Temperature Dropping"}
            ]
        },
        "INDUSTRIAL_ACCIDENT": {
            "name": "Industrial Accident / Hazardous Environment",
            "zone": "ZONE_B",
            "steps": [
                {"gas": 420, "temp": 33.0, "vib": 1.2, "water": 0.0, "desc": "Compressor M-02 Operational Baseline"},
                {"gas": 1600, "temp": 46.0, "vib": 5.4, "water": 0.0, "desc": "Gas Leakage + Mechanical Over-Vibration Spike"},
                {"gas": 2800, "temp": 58.0, "vib": 8.1, "water": 0.0, "desc": "CRITICAL INDUSTRIAL HAZARD - Machine Lockout Triggered"},
                {"gas": 420, "temp": 33.0, "vib": 1.2, "water": 0.0, "desc": "Lockout Resolved - System Nominal"}
            ]
        },
        "GENERAL_EMERGENCY": {
            "name": "General Emergency / Compound Hazard",
            "zone": "ZONE_A",
            "steps": [
                {"gas": 400, "temp": 30.0, "vib": 0.5, "water": 0.0, "desc": "System Nominal"},
                {"gas": 3000, "temp": 52.0, "vib": 7.0, "water": 1.5, "desc": "COMPOUND MULTI-HAZARD CRITICAL EMERGENCY"},
                {"gas": 400, "temp": 30.0, "vib": 0.5, "water": 0.0, "desc": "All Hazards Mitigated"}
            ]
        }
    }

    def __init__(self):
        self.active_scenario: str = None
        self.current_step_idx: int = 0

    def get_available_scenarios(self) -> List[Dict[str, str]]:
        return [
            {"id": key, "name": val["name"], "zone": val["zone"], "steps": len(val["steps"])}
            for key, val in self.SCENARIOS.items()
        ]

    def get_step_telemetry(self, scenario_id: str, step_idx: int) -> Dict[str, Any]:
        scenario = self.SCENARIOS.get(scenario_id, self.SCENARIOS["FIRE_SMOKE"])
        steps = scenario["steps"]
        step_idx = max(0, min(step_idx, len(steps) - 1))
        step = steps[step_idx]

        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "zone_id": scenario["zone"],
            "step_index": step_idx,
            "total_steps": len(steps),
            "description": step["desc"],
            "telemetry": {
                "gas": step["gas"],
                "temperature": step["temp"],
                "vibration": step["vib"],
                "water_level_m": step["water"],
                "humidity": 65.0,
                "pir": 1 if step["gas"] > 1000 else 0,
                "trustScore": 100,
                "is_simulated": True
            }
        }

scenario_engine = ScenarioEngine()
