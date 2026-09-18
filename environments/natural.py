"""
Sentinel-X Environments: Natural Disaster Profile (River Flood & Mountain Landslide)
=====================================================================================
Encapsulates all flood- and natural hazard-specific telemetry, thresholds, and mathematics.
Ensures universal core engines remain clean and environment-independent.
"""

from environments.base import EnvironmentProfile, SensorSpec, HazardRule

natural_profile = EnvironmentProfile(
    id="ENV-NAT-01",
    name="Teesta River Basin & High-Altitude Catchment Zone",
    type="NATURAL",
    location="Sikkim Upper Valley Reach — Gauge Station S-04",
    description="Flash flood, GLOF, and torrential monsoon hydrology monitoring zone.",
    zones=["UPSTREAM_GLACIAL_LAKE", "UPPER_GORGE_GAUGE", "SETTLEMENT_BRIDGE_02", "RUN_OFF_RIDGE"],
    sensors=[
        SensorSpec(sensor_id="RADAR_WATER_LVL", parameter="water_level", unit="meters", zone="UPPER_GORGE_GAUGE", min_limit=0.0, max_limit=30.0, max_rate_change=2.0, default_value=4.8),
        SensorSpec(sensor_id="TIPPING_RAIN_GAUGE", parameter="rainfall_intensity", unit="mm/hr", zone="RUN_OFF_RIDGE", min_limit=0.0, max_limit=250.0, max_rate_change=40.0, default_value=12.0),
        SensorSpec(sensor_id="SOIL_MOISTURE_TDR", parameter="soil_saturation", unit="%", zone="RUN_OFF_RIDGE", min_limit=0.0, max_limit=100.0, max_rate_change=15.0, default_value=55.0),
        SensorSpec(sensor_id="PRESSURE_HEAD", parameter="hydrostatic_head", unit="bar", zone="UPSTREAM_GLACIAL_LAKE", min_limit=0.0, max_limit=10.0, max_rate_change=0.5, default_value=1.4)
    ],
    hazards=[
        HazardRule(hazard_id="HZD-FLASH-FLOOD", name="Flash Flood Surge Warning", category="ENVIRONMENTAL", contributing_parameters=["water_level", "rainfall_intensity"], warning_threshold=8.0, critical_threshold=12.5, severity_weight=1.8),
        HazardRule(hazard_id="HZD-LANDSLIDE", name="Slope Saturated Landslide Trigger", category="ENVIRONMENTAL", contributing_parameters=["soil_saturation", "rainfall_intensity"], warning_threshold=80.0, critical_threshold=92.0, severity_weight=1.5)
    ],
    risk_weights={"water_level": 0.45, "rainfall_intensity": 0.30, "soil_saturation": 0.25},
    response_rules={"HZD-FLASH-FLOOD": "SIREN_DOWNSTREAM_EVACUATION_CIVIL_DEFENSE"},
    communication_profile="HF_SATELLITE_AND_LORA_MESH",
    power_profile="SOLAR_PV_LFP_BATTERY_ISOLATED",
    digital_twin_type="TERRAIN_HYDROLOGY_MESH"
)
