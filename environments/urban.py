"""
Sentinel-X Environments: Urban, Infrastructure, Remote, and Custom Profiles
===========================================================================
"""

from environments.base import EnvironmentProfile, SensorSpec, HazardRule

urban_profile = EnvironmentProfile(
    id="ENV-URB-01",
    name="Smart City Central Transit Underpass & Arterial Flyover",
    type="URBAN",
    location="Delhi NCR Inner Ring Road Sub-Surface Sump",
    description="Low-lying stormwater drainage junction and urban arterial underpass.",
    zones=["UNDERPASS_SUMP", "PUMPING_STATION", "APPROACH_RAMP", "TRAFFIC_PORTAL"],
    sensors=[
        SensorSpec(sensor_id="SUMP_ULTRASONIC", parameter="subsurface_water_depth", unit="cm", zone="UNDERPASS_SUMP", min_limit=0.0, max_limit=300.0, max_rate_change=50.0, default_value=5.0),
        SensorSpec(sensor_id="ROAD_STRUCT_VIB", parameter="deck_vibration_acceleration", unit="mg", zone="APPROACH_RAMP", min_limit=0.0, max_limit=1000.0, max_rate_change=200.0, default_value=45.0),
    ],
    hazards=[
        HazardRule(hazard_id="HZD-URB-INUNDATION", name="Underpass Trapping Inundation", category="INFRASTRUCTURE", contributing_parameters=["subsurface_water_depth"], warning_threshold=40.0, critical_threshold=75.0),
    ],
    risk_weights={"subsurface_water_depth": 0.70, "deck_vibration_acceleration": 0.30},
    response_rules={"HZD-URB-INUNDATION": "LOWER_BOLLARDS_DIVERT_TRAFFIC_ACTIVATE_PUMPS"},
    communication_profile="CELLULAR_5G_OPTICAL_FALLBACK",
    power_profile="MUNICIPAL_GRID_AUTO_GENSET",
    digital_twin_type="URBAN_CITY_BLOCK"
)

infrastructure_profile = EnvironmentProfile(
    id="ENV-INF-01",
    name="Narmada Valley Hydroelectric Dam & Spillway Intake",
    type="INFRASTRUCTURE",
    location="Sardar Sarovar Spillway Structure Block 7",
    description="Heavy concrete gravity dam monitoring structural displacement and reservoir thrust.",
    zones=["CREST_SPILLWAY", "PENSTOCK_INTAKE", "GALLERY_DRAINAGE", "TRANSFORMER_YARD"],
    sensors=[
        SensorSpec(sensor_id="DAM_CRACK_DISPLACEMENT", parameter="joint_opening", unit="mm", zone="GALLERY_DRAINAGE", min_limit=0.0, max_limit=25.0, max_rate_change=1.0, default_value=1.8),
        SensorSpec(sensor_id="PIEZOMETER_PRESSURE", parameter="uplift_pore_pressure", unit="kPa", zone="GALLERY_DRAINAGE", min_limit=0.0, max_limit=800.0, max_rate_change=30.0, default_value=165.0),
    ],
    hazards=[
        HazardRule(hazard_id="HZD-STRUCT-CRACK", name="Spillway Joint Dilation Exceeded", category="INFRASTRUCTURE", contributing_parameters=["joint_opening", "uplift_pore_pressure"], warning_threshold=5.0, critical_threshold=9.0),
    ],
    risk_weights={"joint_opening": 0.60, "uplift_pore_pressure": 0.40},
    response_rules={"HZD-STRUCT-CRACK": "OPEN_RELIEF_VALVES_ALERT_DAM_SAFETY_CORPS"},
    communication_profile="HARDWIRED_SCADA_OPTICAL_SAT_REDUNDANT",
    power_profile="HYDRO_BUS_DUAL_SUBSTATION",
    digital_twin_type="DAM_INFRASTRUCTURE_SOLID"
)

remote_profile = EnvironmentProfile(
    id="ENV-REM-01",
    name="Ladakh High-Altitude Border Weather Observation Post",
    type="REMOTE",
    location="Chang La Pass 5,360m Elevation",
    description="Completely off-grid, sub-zero harsh weather research and emergency post.",
    zones=["METEOROLOGY_MAST", "RADIO_SHELTER", "BATTERY_VAULT"],
    sensors=[
        SensorSpec(sensor_id="WIND_ANEMOMETER", parameter="blizzard_gust_speed", unit="km/h", zone="METEOROLOGY_MAST", min_limit=0.0, max_limit=200.0, max_rate_change=40.0, default_value=28.0),
        SensorSpec(sensor_id="AMBIENT_CRYO_TEMP", parameter="subzero_temp", unit="°C", zone="METEOROLOGY_MAST", min_limit=-50.0, max_limit=30.0, max_rate_change=5.0, default_value=-18.5),
    ],
    hazards=[
        HazardRule(hazard_id="HZD-BLIZZARD-FREEZE", name="Extreme Cryogenic Windchill Blackout", category="ENVIRONMENTAL", contributing_parameters=["blizzard_gust_speed", "subzero_temp"], warning_threshold=80.0, critical_threshold=120.0),
    ],
    risk_weights={"blizzard_gust_speed": 0.50, "subzero_temp": 0.50},
    response_rules={"HZD-BLIZZARD-FREEZE": "SWITCH_HEATED_LITHIUM_BATTERIES_TRANSMIT_HF_BURST"},
    communication_profile="HF_SKY_WAVE_AND_IRIDIUM_SBD",
    power_profile="METHANOL_FUEL_CELL_AND_LTO_CRYOBATTERY",
    digital_twin_type="MOUNTAIN_OUTPOST"
)

custom_profile = EnvironmentProfile(
    id="ENV-CUST-01",
    name="User-Configured Facility",
    type="CUSTOM",
    location="Dynamic Edge Node Site",
    description="Flexible dynamic sensor topology configured on-the-fly.",
    zones=["ZONE_A", "ZONE_B"],
    sensors=[],
    hazards=[],
    risk_weights={},
    response_rules={},
    communication_profile="AUTO_SELECT",
    power_profile="GRID_UPS",
    digital_twin_type="PROCEDURAL_GENERIC"
)
