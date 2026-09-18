"""
Sentinel-X Environments: Indoor Facility Profile (Hospitals, Warehouses, Labs, Data Centers)
=============================================================================================
"""

from environments.base import EnvironmentProfile, SensorSpec, HazardRule

indoor_profile = EnvironmentProfile(
    id="ENV-IND-02",
    name="Apex Logistics Central Fulfillment Hub",
    type="INDOOR",
    location="Sector 62 Mega Logistics Warehouse, Gurugram",
    description="Automated high-rack warehouse facility with AGV lanes and cold-chain zones.",
    zones=["HIGH_RACK_STORAGE", "AGV_CORRIDOR", "PACKING_STATION", "SERVER_ROOM", "BATTERY_CHARGING_BAY"],
    sensors=[
        SensorSpec(sensor_id="MQ2_SMOKE", parameter="smoke_density", unit="ppm", zone="SERVER_ROOM", min_limit=0.0, max_limit=500.0, max_rate_change=20.0, default_value=12.0),
        SensorSpec(sensor_id="BME680_TEMP", parameter="room_temperature", unit="°C", zone="HIGH_RACK_STORAGE", min_limit=-10.0, max_limit=60.0, max_rate_change=2.0, default_value=22.5),
        SensorSpec(sensor_id="WATER_LEAK_ROPE", parameter="water_leakage", unit="binary", zone="SERVER_ROOM", min_limit=0.0, max_limit=1.0, max_rate_change=1.0, default_value=0.0),
        SensorSpec(sensor_id="PIR_OCCUPANCY", parameter="occupancy_count", unit="persons", zone="AGV_CORRIDOR", min_limit=0.0, max_limit=50.0, max_rate_change=10.0, default_value=4.0),
    ],
    hazards=[
        HazardRule(hazard_id="HZD-FIRE-SMOKE", name="Internal Fire & Smoke Spread", category="ENVIRONMENTAL", contributing_parameters=["smoke_density", "room_temperature"], warning_threshold=45.0, critical_threshold=100.0),
        HazardRule(hazard_id="HZD-WATER-FLOOD", name="Data Center Water Ingress", category="INFRASTRUCTURE", contributing_parameters=["water_leakage"], warning_threshold=0.5, critical_threshold=0.9),
    ],
    risk_weights={"smoke_density": 0.40, "room_temperature": 0.30, "water_leakage": 0.30},
    response_rules={"HZD-FIRE-SMOKE": "FIRE_SUPPRESSION_AND_BUILDING_EVAC", "HZD-WATER-FLOOD": "POWER_ISOLATION_VALVE_SHUT"},
    communication_profile="WIFI6_MESH_AND_ETHERNET",
    power_profile="DUAL_UPS_DIESEL_GENSET",
    digital_twin_type="FACILITY_BUILDING"
)
