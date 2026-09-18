"""
Sentinel-X SIH 2026 Grand Finale Demonstration Engine
=====================================================
Executes the exact 23-step demonstration sequence specified in Section 26 of the
Master Engineering Specification:
  1. System normal
  2. Show live ESP32 sensor telemetry
  3. Show conveyor digital twin
  4. Increase motor temperature (trend detection)
  5. Increase vibration (bearing cross-evidence)
  6. Risk increases to WARNING
  7. Inject false sensor (spoofed thermal jump)
  8. Trust engine detects inconsistent sensor
  9. Sensor quarantined (loses voting authority)
  10. Worker enters danger zone
  11. Critical alarm (E-Stop trip, red strobe, 110dB horn)
  12. Disconnect Internet (DEGRADED state)
  13. Communication switches to HF simulation (7.105 MHz AX.25)
  14. Disable all communication (ISOLATED state)
  15. Local safety continues without cloud
  16. Events accumulate on USB pendrive
  17. Restore communication (RECOVERY state)
  18. Store-and-forward synchronization
  19. Open instant digital twin builder
  20. Import industrial photographs
  21. Generate photo-assisted digital twin
  22. Anchor sensor data to reconstructed objects
  23. Complete operational digital twin
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class DemoStepState(BaseModel):
    step_number: int
    title: str
    description: str
    telemetry_state: Dict[str, Any]
    trust_scores: Dict[str, float]
    quarantined_sensors: List[str]
    risk_score: float
    risk_level: str # NORMAL, WATCH, WARNING, CRITICAL
    actuators: Dict[str, Any]
    communication_state: str # NORMAL, DEGRADED, EMERGENCY, ISOLATED, RECOVERY
    store_and_forward_pending: int
    digital_twin_mode: str # BASELINE_SCENE, FALSE_SENSOR_HIGHLIGHT, CRITICAL_TRIP, RECONSTRUCTED_TWIN

class SIHDemoEngine:
    def __init__(self):
        self.current_step = 1

    def get_step_state(self, step: int) -> DemoStepState:
        s = max(1, min(27, step))
        self.current_step = s

        # Step-specific parameters
        if s == 1:
            return DemoStepState(
                step_number=1,
                title="System Normal Baseline",
                description="Conveyor operating nominal. RPi 5 edge brain active, SQLite WAL logging nominal telemetry.",
                telemetry_state={"motor_temp": 68.5, "vibration": 2.4, "current": 48.2, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "ACS712_CURRENT": 95.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=12.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 2:
            return DemoStepState(
                step_number=2,
                title="ESP32-S3 Live Sensor Telemetry Ingestion",
                description="Distributed FreeRTOS sensing nodes publishing verified telemetry frames via local MQTT.",
                telemetry_state={"motor_temp": 69.1, "vibration": 2.5, "current": 48.8, "worker_dist": 4.2, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "ACS712_CURRENT": 95.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=14.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 3:
            return DemoStepState(
                step_number=3,
                title="Conveyor Digital Twin Telemetry Binding",
                description="3D scene objects bound to live ESP32 sensor streams with physics and wear mapping.",
                telemetry_state={"motor_temp": 70.0, "vibration": 2.6, "current": 49.0, "worker_dist": 4.0, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "ACS712_CURRENT": 95.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=15.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 4:
            return DemoStepState(
                step_number=4,
                title="Motor Temperature Rise Detected",
                description="Drive motor winding temperature trending upward to 79.5°C. Early thermal advisory logged.",
                telemetry_state={"motor_temp": 79.5, "vibration": 3.1, "current": 54.2, "worker_dist": 3.8, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 97.0, "ADXL345_VIBRATION": 96.0, "ACS712_CURRENT": 95.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=38.0,
                risk_level="WATCH",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 5:
            return DemoStepState(
                step_number=5,
                title="Bearing Vibration Surge (Cross-Sensor Evidence)",
                description="ADXL345 detects bearing vibration spike to 5.8 mm/s RMS. Multi-sensor fusion engine correlates heat + vibration.",
                telemetry_state={"motor_temp": 82.0, "vibration": 5.8, "current": 58.0, "worker_dist": 3.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 96.0, "ADXL345_VIBRATION": 95.0, "ACS712_CURRENT": 94.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=62.0,
                risk_level="WARNING",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 6:
            return DemoStepState(
                step_number=6,
                title="Risk Engine Elevates State to WARNING",
                description="Generic risk engine computes aggregate mechanical risk of 68.0. Automatic speed derate triggered.",
                telemetry_state={"motor_temp": 84.5, "vibration": 6.2, "current": 52.0, "worker_dist": 3.4, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "ACS712_CURRENT": 94.0, "TOF_LIDAR": 97.0},
                quarantined_sensors=[],
                risk_score=68.0,
                risk_level="WARNING",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 7:
            return DemoStepState(
                step_number=7,
                title="False Sensor Spoofing Attack Injected",
                description="Fault injection: SENSOR_TEMP_AUX_B suddenly reports 140°C in 0.1s without corroboration from neighbor sensors.",
                telemetry_state={"motor_temp": 84.5, "spoofed_temp": 140.0, "vibration": 6.2, "current": 52.0, "worker_dist": 3.4, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "SENSOR_TEMP_AUX_B": 48.0, "ADXL345_VIBRATION": 95.0, "ACS712_CURRENT": 94.0},
                quarantined_sensors=[],
                risk_score=68.0,
                risk_level="WARNING",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="FALSE_SENSOR_HIGHLIGHT"
            )
        elif s == 8:
            return DemoStepState(
                step_number=8,
                title="Trust Engine Detects Anomaly & Inconsistency",
                description="Rate-of-change physics jump check and cross-sensor peer voting detect SENSOR_TEMP_AUX_B as an outlier.",
                telemetry_state={"motor_temp": 84.5, "spoofed_temp": 140.0, "vibration": 6.2, "current": 52.0, "worker_dist": 3.4, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "SENSOR_TEMP_AUX_B": 18.0, "ADXL345_VIBRATION": 95.0, "ACS712_CURRENT": 94.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=68.0,
                risk_level="WARNING",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="FALSE_SENSOR_HIGHLIGHT"
            )
        elif s == 9:
            return DemoStepState(
                step_number=9,
                title="Sensor Quarantined — Voting Rights Revoked",
                description="Byzantine quarantine isolates spoofed sensor with weight=0.0. Prevents false plant shutdown.",
                telemetry_state={"motor_temp": 84.5, "vibration": 6.2, "current": 52.0, "worker_dist": 3.4, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "SENSOR_TEMP_AUX_B": 0.0, "ADXL345_VIBRATION": 95.0, "ACS712_CURRENT": 94.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=68.0,
                risk_level="WARNING",
                actuators={"motor_relay": True, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 10:
            return DemoStepState(
                step_number=10,
                title="Worker Enters Danger Nip-Point Zone",
                description="ToF LiDAR detects worker breach into restricted rotating conveyor zone (distance < 0.8m while motor energized).",
                telemetry_state={"motor_temp": 84.5, "vibration": 6.2, "current": 52.0, "worker_dist": 0.65, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=96.0,
                risk_level="CRITICAL",
                actuators={"motor_relay": False, "beacon": "RED", "siren_db": 95, "e_stop": True},
                communication_state="NORMAL",
                store_and_forward_pending=1,
                digital_twin_mode="CRITICAL_TRIP"
            )
        elif s == 11:
            return DemoStepState(
                step_number=11,
                title="Autonomous Hardware Emergency Trip Initiated",
                description="RPi 5 cuts motor power relay locally in <8.4ms. Red strobe and 95dB horn fired directly on edge.",
                telemetry_state={"motor_temp": 84.0, "vibration": 0.2, "current": 0.0, "worker_dist": 0.65, "estop": 1},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=98.0,
                risk_level="CRITICAL",
                actuators={"motor_relay": False, "beacon": "RED", "siren_db": 95, "e_stop": True},
                communication_state="NORMAL",
                store_and_forward_pending=2,
                digital_twin_mode="CRITICAL_TRIP"
            )
        elif s == 12:
            return DemoStepState(
                step_number=12,
                title="Infrastructure Failure: Internet WAN Severed",
                description="Fiber cut simulated. WAN connection lost. Local intelligence continues unabated on RPi 5.",
                telemetry_state={"motor_temp": 82.0, "vibration": 0.1, "current": 0.0, "worker_dist": 1.2, "estop": 1},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=85.0,
                risk_level="CRITICAL",
                actuators={"motor_relay": False, "beacon": "RED", "siren_db": 95, "e_stop": True},
                communication_state="DEGRADED",
                store_and_forward_pending=4,
                digital_twin_mode="CRITICAL_TRIP"
            )
        elif s == 13:
            return DemoStepState(
                step_number=13,
                title="Failover to HF Packet Radio Simulation",
                description="Communication manager activates 7.105 MHz AX.25 packet radio emergency channel.",
                telemetry_state={"motor_temp": 80.0, "vibration": 0.1, "current": 0.0, "worker_dist": 1.8, "estop": 1},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=78.0,
                risk_level="CRITICAL",
                actuators={"motor_relay": False, "beacon": "RED", "siren_db": 0, "e_stop": True},
                communication_state="EMERGENCY",
                store_and_forward_pending=5,
                digital_twin_mode="CRITICAL_TRIP"
            )
        elif s == 14:
            return DemoStepState(
                step_number=14,
                title="Total Electromagnetic Blackout (ISOLATED Mode)",
                description="All RF, cellular, and internet channels severed. System enters complete autonomous isolation.",
                telemetry_state={"motor_temp": 76.0, "vibration": 0.0, "current": 0.0, "worker_dist": 3.0, "estop": 1},
                trust_scores={"PT100_MOTOR_TEMP": 95.0, "ADXL345_VIBRATION": 95.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=["SENSOR_TEMP_AUX_B"],
                risk_score=60.0,
                risk_level="WARNING",
                actuators={"motor_relay": False, "beacon": "YELLOW", "siren_db": 0, "e_stop": True},
                communication_state="ISOLATED",
                store_and_forward_pending=8,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 15:
            return DemoStepState(
                step_number=15,
                title="Local Safety & Sensor Monitoring Continues",
                description="'When infrastructure fails, safety continues.' RPi 5 maintains full sensor loops and local alarms.",
                telemetry_state={"motor_temp": 72.0, "vibration": 0.0, "current": 0.0, "worker_dist": 3.8, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 96.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=35.0,
                risk_level="WATCH",
                actuators={"motor_relay": False, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="ISOLATED",
                store_and_forward_pending=12,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 16:
            return DemoStepState(
                step_number=16,
                title="Events Accumulate in USB Pendrive Resilient Store",
                description="Events saved with sequence numbers in /sentinel-data/ USB store under SQLite WAL format.",
                telemetry_state={"motor_temp": 70.0, "vibration": 0.0, "current": 0.0, "worker_dist": 4.0, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 97.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=25.0,
                risk_level="WATCH",
                actuators={"motor_relay": False, "beacon": "YELLOW", "siren_db": 0, "e_stop": False},
                communication_state="ISOLATED",
                store_and_forward_pending=18,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 17:
            return DemoStepState(
                step_number=17,
                title="Communication Restored (RECOVERY State)",
                description="WAN and optical links re-established. Communication manager initiates recovery protocol.",
                telemetry_state={"motor_temp": 69.0, "vibration": 0.0, "current": 0.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=18.0,
                risk_level="NORMAL",
                actuators={"motor_relay": False, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="RECOVERY",
                store_and_forward_pending=18,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 18:
            return DemoStepState(
                step_number=18,
                title="Ordered Store-and-Forward Synchronization",
                description="18 queued events flushed from USB pendrive to command center. Zero silent loss verified.",
                telemetry_state={"motor_temp": 68.8, "vibration": 0.0, "current": 0.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=15.0,
                risk_level="NORMAL",
                actuators={"motor_relay": False, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 19:
            return DemoStepState(
                step_number=19,
                title="Open Instant Digital Twin Builder",
                description="Accessing photo-assisted facility digital twin builder interface.",
                telemetry_state={"motor_temp": 68.5, "vibration": 2.4, "current": 48.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=12.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 20:
            return DemoStepState(
                step_number=20,
                title="Importing 5 Industrial Plant Photographs",
                description="Loading multi-view photos of Bokaro sinter conveyor drive unit into reconstruction pipeline.",
                telemetry_state={"motor_temp": 68.5, "vibration": 2.4, "current": 48.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=12.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 21:
            return DemoStepState(
                step_number=21,
                title="Generating Photo-Assisted 3D Geometry",
                description="Extracting spatial keypoints and semantic object bounding boxes. (Method: Photo-Assisted Procedural).",
                telemetry_state={"motor_temp": 68.5, "vibration": 2.4, "current": 48.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=12.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )
        elif s == 22:
            return DemoStepState(
                step_number=22,
                title="Anchoring Sensor Nodes to Reconstructed Objects",
                description="Binding ESP32 PT100 temperature to Motor M007 and ADXL345 vibration to Bearing B-101.",
                telemetry_state={"motor_temp": 68.5, "vibration": 2.4, "current": 48.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=12.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )
        elif s == 23:
            return DemoStepState(
                step_number=23,
                title="Store-and-Forward Synchronized",
                description="Communication restored to EOC; 37 queued offline events successfully synchronized with zero data loss.",
                telemetry_state={"motor_temp": 48.0, "vibration": 1.4, "current": 28.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=10.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="RECOVERY",
                store_and_forward_pending=0,
                digital_twin_mode="BASELINE_SCENE"
            )
        elif s == 24:
            return DemoStepState(
                step_number=24,
                title="Import Industrial Multi-Angle Photographs",
                description="Loading 5 field validation photographs (0° Front, 45° Oblique, 90° Profile, Top-Down, Macro Bearing).",
                telemetry_state={"motor_temp": 48.0, "vibration": 1.4, "current": 28.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=10.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )
        elif s == 25:
            return DemoStepState(
                step_number=25,
                title="Generate Photo-Assisted Industrial Digital Twin",
                description="5-Stage photogrammetry pipeline executes: SIFT Keypoints -> Epipolar SfM -> DeepLabV3+ -> Poisson Meshing.",
                telemetry_state={"motor_temp": 48.0, "vibration": 1.4, "current": 28.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=10.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )
        elif s == 26:
            return DemoStepState(
                step_number=26,
                title="Bind Sensor Telemetry to Digital Twin Objects",
                description="Binding ESP32 PT100 temperature to MOTOR-01, ADXL345 vibration to BEARING-01, and ToF LiDAR to Danger Zone.",
                telemetry_state={"motor_temp": 48.0, "vibration": 1.4, "current": 28.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=10.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )
        else: # Step 27
            return DemoStepState(
                step_number=27,
                title="Inspect MOTOR-01 Object: Live Telemetry, Trust & History",
                description="Operator clicks MOTOR-01: Displays live telemetry (48.0°C), Byzantine trust (98%), risk score (10.0), and complete provenance.",
                telemetry_state={"motor_temp": 48.0, "vibration": 1.4, "current": 28.0, "worker_dist": 4.5, "estop": 0},
                trust_scores={"PT100_MOTOR_TEMP": 98.0, "ADXL345_VIBRATION": 96.0, "TOF_LIDAR": 98.0},
                quarantined_sensors=[],
                risk_score=10.0,
                risk_level="NORMAL",
                actuators={"motor_relay": True, "beacon": "GREEN", "siren_db": 0, "e_stop": False},
                communication_state="NORMAL",
                store_and_forward_pending=0,
                digital_twin_mode="RECONSTRUCTED_TWIN"
            )

sih_demo_engine = SIHDemoEngine()
