"""
Sentinel-X Environments: Flagship Industrial Manufacturing / Conveyor Profile
=============================================================================
Primary demonstration environment for Smart India Hackathon 2026.
Represents a heavy industrial material handling conveyor plant:
  - 45 kW 3-phase AC induction drive motor (M007)
  - 2-stage helical reduction gearbox (GB-02)
  - 24-meter heavy rubberized bulk conveyor belt (CV-LINE-1)
  - High-wear cylindrical roller bearings (B-101 / B-102)
  - Guarded worker maintenance & operator stations
  - Restricted hazardous pinch-point zone with ToF optical barriers
  - Emergency pull-wire interlock & acoustic-visual warning tower
"""

from environments.base import EnvironmentProfile, SensorSpec, HazardRule

industrial_profile = EnvironmentProfile(
    id="ENV-IND-01",
    name="Tata Heavy Industries — Raw Material Conveyor Line 4",
    type="INDUSTRIAL",
    location="Bokaro Steel Sinter Plant — Unit 4 Bay C",
    description="Operational 24-meter heavy bulk material conveyor handling iron ore sinter.",
    zones=[
        "DRIVE_MOTOR_BAY",
        "GEARBOX_ASSEMBLY",
        "HEAD_DISCHARGE_PULLEY",
        "TAIL_TENSION_PULLEY",
        "RESTRICTED_PINCH_ZONE",
        "OPERATOR_CONTROL_CABIN",
        "ELECTRICAL_MCC_ROOM"
    ],
    sensors=[
        SensorSpec(
            sensor_id="PT100_MOTOR_TEMP",
            parameter="motor_temperature",
            unit="°C",
            zone="DRIVE_MOTOR_BAY",
            min_limit=0.0,
            max_limit=140.0,
            max_rate_change=4.0,
            default_value=68.5,
            data_source="LIVE" # Flagship demonstration sensor
        ),
        SensorSpec(
            sensor_id="ADXL345_VIBRATION",
            parameter="bearing_vibration",
            unit="mm/s RMS",
            zone="DRIVE_MOTOR_BAY",
            min_limit=0.0,
            max_limit=25.0,
            max_rate_change=5.0,
            default_value=2.4,
            data_source="LIVE"
        ),
        SensorSpec(
            sensor_id="ACS712_CURRENT",
            parameter="motor_current",
            unit="A",
            zone="ELECTRICAL_MCC_ROOM",
            min_limit=0.0,
            max_limit=120.0,
            max_rate_change=25.0,
            default_value=48.2,
            data_source="LIVE"
        ),
        SensorSpec(
            sensor_id="GEARBOX_TEMP",
            parameter="gearbox_temperature",
            unit="°C",
            zone="GEARBOX_ASSEMBLY",
            min_limit=0.0,
            max_limit=110.0,
            max_rate_change=3.0,
            default_value=62.0,
            data_source="SIMULATED"
        ),
        SensorSpec(
            sensor_id="BELT_SPEED_ENCODER",
            parameter="belt_speed",
            unit="m/s",
            zone="HEAD_DISCHARGE_PULLEY",
            min_limit=0.0,
            max_limit=4.0,
            max_rate_change=1.5,
            default_value=2.2,
            data_source="SIMULATED"
        ),
        SensorSpec(
            sensor_id="TOF_LIDAR_PROXIMITY",
            parameter="worker_proximity",
            unit="m",
            zone="RESTRICTED_PINCH_ZONE",
            min_limit=0.0,
            max_limit=8.0,
            max_rate_change=6.0,
            default_value=4.5,
            data_source="SIMULATED"
        ),
        SensorSpec(
            sensor_id="ESTOP_PULL_WIRE",
            parameter="estop_state",
            unit="binary",
            zone="RESTRICTED_PINCH_ZONE",
            min_limit=0.0,
            max_limit=1.0,
            max_rate_change=1.0,
            default_value=0.0,
            data_source="SIMULATED"
        ),
        SensorSpec(
            sensor_id="MQ135_GAS_SMOKE",
            parameter="smoke_gas_ppm",
            unit="ppm",
            zone="DRIVE_MOTOR_BAY",
            min_limit=0.0,
            max_limit=1000.0,
            max_rate_change=50.0,
            default_value=18.0,
            data_source="SIMULATED"
        )
    ],
    hazards=[
        HazardRule(
            hazard_id="HZD-MTR-HEAT",
            name="Motor Winding Overheating",
            category="MECHANICAL",
            contributing_parameters=["motor_temperature", "motor_current"],
            warning_threshold=80.0,
            critical_threshold=95.0,
            severity_weight=1.2
        ),
        HazardRule(
            hazard_id="HZD-BRG-DEG",
            name="Bearing Mechanical Degradation",
            category="MECHANICAL",
            contributing_parameters=["bearing_vibration", "motor_temperature"],
            warning_threshold=5.5,
            critical_threshold=8.0,
            severity_weight=1.4
        ),
        HazardRule(
            hazard_id="HZD-WRK-ZONE",
            name="Worker Intrusion in Restricted Pinch Zone",
            category="HUMAN",
            contributing_parameters=["worker_proximity", "belt_speed"],
            warning_threshold=1.8, # meters
            critical_threshold=0.8,
            severity_weight=2.0
        ),
        HazardRule(
            hazard_id="HZD-ESTOP-TRIP",
            name="Emergency Stop Pull-Wire Circuit Tripped",
            category="HUMAN",
            contributing_parameters=["estop_state"],
            warning_threshold=0.5,
            critical_threshold=0.9,
            severity_weight=2.5
        ),
        HazardRule(
            hazard_id="HZD-ELEC-FIRE",
            name="Electrical Overload / Insulation Smoke",
            category="ENVIRONMENTAL",
            contributing_parameters=["smoke_gas_ppm", "motor_current"],
            warning_threshold=80.0,
            critical_threshold=180.0,
            severity_weight=1.5
        )
    ],
    risk_weights={
        "motor_temperature": 0.25,
        "bearing_vibration": 0.25,
        "worker_proximity": 0.30,
        "motor_current": 0.10,
        "smoke_gas_ppm": 0.10
    },
    response_rules={
        "HZD-WRK-ZONE": "EMERGENCY_STOP_AND_RED_STROBE",
        "HZD-MTR-HEAT": "SPEED_DERATE_AND_YELLOW_BEACON",
        "HZD-BRG-DEG": "MAINTENANCE_LOG_AND_YELLOW_BEACON",
        "HZD-ESTOP-TRIP": "HARDWARE_CUT_AND_110DB_SIREN"
    },
    communication_profile="HIGH_BANDWIDTH_ETHERNET_AND_LOCAL_MQTT",
    power_profile="415V_3PHASE_INDUSTRIAL_UPS",
    digital_twin_type="CONVEYOR_3D_SCADA"
)
