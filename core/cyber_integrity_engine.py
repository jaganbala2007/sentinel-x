"""
Sentinel-X Cyber-Integrity & Attack Simulation Engine
======================================================
Provides safe, defensive detection and demonstration capabilities for industrial
data-manipulation and telemetry spoofing attacks (e.g. Stuxnet-style false low telemetry).

Hero Scenario 1:
    - Real Physical Machine Temperature: 82.0°C
    - Simulated Manipulated PLC Value: 42.0°C
    - Independent Thermal Camera: 81.4°C (Trust 97%)
    - Aux Sensor B: 80.8°C (Trust 92%)
    - Motor Current & Vibration: HIGH (Plausibility violation detected)
    - Cross-sensor Conflict Detected -> PLC Trust degraded to 37%
    - True State Recovery: ~81.2°C -> Machine Risk CRITICAL -> Automated Safe Response
"""

from typing import Dict, Any, List
from datetime import datetime
from core.trust_engine import trust_engine, SensorObservation


class CyberIntegrityEngine:
    def __init__(self):
        self.attack_simulation_active: bool = False
        self.active_scenario_name: str = "NONE"
        self.last_evaluation_result: Dict[str, Any] = {}

    def run_hero_scenario_1(self, simulate_manipulation: bool = True) -> Dict[str, Any]:
        """
        Executes the primary Hero Demo 1 scenario.
        """
        self.attack_simulation_active = simulate_manipulation
        self.active_scenario_name = "PLC_FALSE_LOW_TEMPERATURE_SPOOFING" if simulate_manipulation else "NORMAL_OPERATION"

        real_physical_temp = 82.0
        reported_plc_temp = 42.0 if simulate_manipulation else 70.5
        camera_temp = 81.4 if simulate_manipulation else 70.8
        aux_temp = 80.8 if simulate_manipulation else 70.2

        motor_current = 48.5 if simulate_manipulation else 28.0
        vibration_rms = 8.4 if simulate_manipulation else 2.1
        rpm = 2950.0

        # Construct multi-source sensor observations for Machine M-007
        observations = [
            SensorObservation(
                parameter="temperature",
                value=reported_plc_temp,
                unit="°C",
                source="PLC_MODBUS_CHANNEL_01",
                device_id="PLC_TEMP_M007"
            ),
            SensorObservation(
                parameter="temperature",
                value=camera_temp,
                unit="°C",
                source="CALIBRATED_THERMAL_IMAGER",
                device_id="THERMAL_CAM_01"
            ),
            SensorObservation(
                parameter="temperature",
                value=aux_temp,
                unit="°C",
                source="ISOLATED_ANALOG_RTD_B",
                device_id="SENSOR_TEMP_AUX_B"
            )
        ]

        # 1. Evaluate Sensor Consensus
        consensus = trust_engine.evaluate_sensor_consensus("Machine M-007 Bearing Temperature", observations)

        # 2. Evaluate Physical Plausibility (Current + Vibration vs Reported PLC Temp)
        is_plausible, plausibility_warnings = trust_engine.check_physical_plausibility({
            "temperature": reported_plc_temp,
            "current": motor_current,
            "vibration": vibration_rms,
            "rpm": rpm,
            "power_state": 1.0
        })

        # 3. Determine True State & Risk Level
        trusted_temp = consensus["trusted_value"]
        plc_trust_score = trust_engine.get_device_trust("PLC_TEMP_M007")

        if simulate_manipulation:
            risk_level = "CRITICAL"
            risk_score = 91.5
            safety_state = "DATA_INTEGRITY_VIOLATION_AND_OVERHEATING"
            recommendations = [
                "IMMEDIATE ACTION: Restrict personnel access to Zone-B (Machine M-007 perimeter).",
                "Quarantine PLC_TEMP_M007 telemetry stream due to confirmed cross-sensor conflict.",
                "Switch Digital Twin state estimation to Calibrated Thermal Imager (81.4°C).",
                "Dispatch Field Maintenance for emergency thermal inspection & PLC integrity audit."
            ]
        else:
            risk_level = "SAFE"
            risk_score = 12.0
            safety_state = "NOMINAL_OPERATION"
            recommendations = [
                "Machine M-007 operating within nominal thermodynamic envelopes.",
                "All telemetry channels verified consistent."
            ]

        result = {
            "scenario": self.active_scenario_name,
            "simulation_active": self.attack_simulation_active,
            "target_machine": "M-007 (High-Pressure Compressor)",
            "zone": "Zone-B",
            "physical_reality": {
                "actual_temperature": real_physical_temp if simulate_manipulation else 70.0,
                "motor_current_amps": motor_current,
                "vibration_mm_s": vibration_rms,
                "rpm": rpm,
                "status": "SEVERE_OVERHEATING" if simulate_manipulation else "NOMINAL"
            },
            "reported_telemetry": {
                "plc_reported_temperature": reported_plc_temp,
                "plc_trust_score": plc_trust_score,
                "thermal_camera_temperature": camera_temp,
                "thermal_camera_trust_score": trust_engine.get_device_trust("THERMAL_CAM_01"),
                "aux_rtd_temperature": aux_temp,
                "aux_rtd_trust_score": trust_engine.get_device_trust("SENSOR_TEMP_AUX_B")
            },
            "sensor_consensus": consensus,
            "physical_plausibility": {
                "is_plausible": is_plausible,
                "warnings": plausibility_warnings
            },
            "estimated_true_state": {
                "temperature": trusted_temp,
                "unit": "°C",
                "confidence": consensus["confidence"],
                "data_state": "ESTIMATED_VIA_CONSENSUS" if simulate_manipulation else "MEASURED_VERIFIED"
            },
            "risk_evaluation": {
                "score": risk_score,
                "level": risk_level,
                "safety_state": safety_state,
                "primary_threat": "UNAUTHORIZED_TELEMETRY_SPOOFING_MASKING_CRITICAL_OVERHEAT" if simulate_manipulation else "NONE"
            },
            "decision_engine_output": {
                "urgency": "CRITICAL" if simulate_manipulation else "LOW",
                "automated_override_triggered": simulate_manipulation,
                "affected_assets": ["M-007", "Zone-B", "WRK-014"],
                "recommendations": recommendations
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        self.last_evaluation_result = result
        return result

    def reset_simulation(self) -> Dict[str, Any]:
        """Resets simulation and restores all device trust baselines."""
        self.attack_simulation_active = False
        self.active_scenario_name = "NONE"
        trust_engine.reset_device_trust()
        return self.run_hero_scenario_1(simulate_manipulation=False)


cyber_integrity_engine = CyberIntegrityEngine()
