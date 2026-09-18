"""
Sentinel-X V2 Environment Router
================================
Endpoints for discovering, switching, and evaluating Environment Profiles:
  - INDUSTRIAL: Raw Material Conveyor 4 (Flagship)
  - INDOOR: Apex Logistics Fulfillment Hub
  - NATURAL: Teesta River Flood Basin & Mountain Hydrology
  - URBAN: Transit Underpass Sump & Flyover
  - INFRASTRUCTURE: Narmada Hydro Dam & Spillway
  - REMOTE: Ladakh Chang La High-Altitude Post
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.schemas.universal import (
    EnvironmentProfile,
    EnvironmentType,
    MultiHazardRiskAssessment,
    NormalizedSensorReading
)
from app.services.environment_manager import environment_manager
from app.services.universal_risk_engine import universal_risk_engine
from environments import environment_registry

router = APIRouter(prefix="/api/v1/environment", tags=["Environment Profiles & Multi-Hazard Intelligence"])

# Map frontend short codes to internal profiles and digital twins
ENV_METADATA = {
    "INDUSTRIAL": {
        "id": "INDUSTRIAL",
        "name": "Tata Heavy Industries — Raw Material Conveyor 4",
        "type": "INDUSTRIAL",
        "location": "Bokaro Steel Sinter Plant — Unit 4 Bay C",
        "description": "Operational 24-meter heavy bulk material conveyor handling iron ore sinter with 45 kW motor M007.",
        "digital_twin_type": "FLAGSHIP_CONVEYOR_SCADA",
        "camera_preset": {"pos": [-6.5, 4.5, 8.5], "target": [0, 0.8, 0]},
        "sensors": [
            {"id": "PT100_MOTOR_TEMP", "name": "Motor M007 Winding Temp", "param": "motor_temperature", "unit": "°C", "normal": 68.5, "warning": 80.0, "critical": 90.0, "current": 68.5},
            {"id": "ADXL345_VIB", "name": "Drive Bearing Vibration", "param": "bearing_vibration", "unit": "mm/s", "normal": 2.4, "warning": 4.5, "critical": 7.2, "current": 2.4},
            {"id": "ACS712_CURRENT", "name": "Drive Motor 3-Phase Current", "param": "motor_current", "unit": "A", "normal": 48.2, "warning": 65.0, "critical": 82.0, "current": 48.2},
            {"id": "TOF_LIDAR", "name": "Pinch-Point Worker Barrier", "param": "worker_proximity", "unit": "m", "normal": 4.5, "warning": 1.5, "critical": 0.8, "current": 4.5}
        ],
        "hazards": ["Bearing Mechanical Degradation (ISO 10816)", "Motor Winding Thermal Runaway", "Human-Machine Pinch Conflict", "Emergency Pull-Wire Trip"],
        "default_risk": 12.0,
        "default_level": "NORMAL"
    },
    "INDOOR": {
        "id": "INDOOR",
        "name": "Apex Logistics Fulfillment Hub — High-Bay Warehouse",
        "type": "INDOOR",
        "location": "Bhiwandi E-Commerce Logistics Corridor — Facility 3",
        "description": "250,000 sq ft automated sorting hub with high-bay shelving, AGV corridors, and high-density worker zones.",
        "digital_twin_type": "WAREHOUSE_FULFILLMENT_SCADA",
        "camera_preset": {"pos": [-8.0, 7.0, 10.0], "target": [0, 1.5, 0]},
        "sensors": [
            {"id": "OPTICAL_SMOKE_01", "name": "High-Bay Particulate Smoke", "param": "smoke_density", "unit": "%/m", "normal": 0.2, "warning": 1.5, "critical": 4.0, "current": 0.2},
            {"id": "AMB_TEMP_ROOF", "name": "Stairwell & Roof Thermal", "param": "ambient_temp", "unit": "°C", "normal": 26.5, "warning": 45.0, "critical": 65.0, "current": 26.5},
            {"id": "MQ135_AIR_QUAL", "name": "CO / Toxic Combustion Gas", "param": "co_gas_ppm", "unit": "ppm", "normal": 12.0, "warning": 25.0, "critical": 50.0, "current": 12.0},
            {"id": "HVAC_FLOW_SENSOR", "name": "Exhaust Airflow Velocity", "param": "exhaust_flow", "unit": "m/s", "normal": 4.8, "warning": 2.0, "critical": 0.5, "current": 4.8}
        ],
        "hazards": ["High-Bay Combustible Fire", "Smoke Stairwell Infiltration", "Toxic Gas Accumulation", "Power / Ventilation Loss"],
        "default_risk": 8.0,
        "default_level": "NORMAL"
    },
    "NATURAL": {
        "id": "NATURAL",
        "name": "Teesta River Flood Basin & Mountain Hydrology",
        "type": "NATURAL",
        "location": "Sikkim-Bengal Boundary River Gauge Station 04",
        "description": "Dynamic glacial melt and cloudburst river basin monitoring upstream flash-flood surges.",
        "digital_twin_type": "WATERSHED_RIVER_SCADA",
        "camera_preset": {"pos": [-10.0, 9.0, 12.0], "target": [0, 1.0, 0]},
        "sensors": [
            {"id": "RADAR_WATER_LVL", "name": "River Stage Hydrology", "param": "water_level_m", "unit": "m", "normal": 2.41, "warning": 3.20, "critical": 3.85, "current": 2.41},
            {"id": "DOPPLER_FLOW_RATE", "name": "Rate of Water Rise", "param": "rate_of_rise", "unit": "m/min", "normal": 0.01, "warning": 0.04, "critical": 0.08, "current": 0.01},
            {"id": "BARO_BMP390", "name": "Barometric Depression", "param": "baro_pressure", "unit": "hPa", "normal": 1012.5, "warning": 990.0, "critical": 975.0, "current": 1012.5},
            {"id": "SOIL_MOISTURE_TDR", "name": "Valley Soil Saturation", "param": "soil_saturation", "unit": "%", "normal": 48.0, "warning": 80.0, "critical": 95.0, "current": 48.0}
        ],
        "hazards": ["Glacial Lake Outburst Surge (GLOF)", "Mountain Basin Flash Flood", "Steep Terrain Landslide", "Flash Gauge Debris Collision"],
        "default_risk": 15.0,
        "default_level": "NORMAL"
    },
    "URBAN": {
        "id": "URBAN",
        "name": "Smart City Central Transit Underpass & Sump",
        "type": "URBAN",
        "location": "Delhi NCR Inner Ring Road Sub-Surface Sump",
        "description": "Depressed roadway underpass prone to monsoon inundation and vehicle trapping.",
        "digital_twin_type": "URBAN_UNDERPASS_SCADA",
        "camera_preset": {"pos": [-7.5, 5.0, 9.0], "target": [0, 0.5, 0]},
        "sensors": [
            {"id": "SUMP_ULTRASONIC", "name": "Underpass Sump Depth", "param": "sump_depth_cm", "unit": "cm", "normal": 5.0, "warning": 40.0, "critical": 75.0, "current": 5.0},
            {"id": "FLYOVER_DECK_VIB", "name": "Flyover Deck Acceleration", "param": "deck_vib_mg", "unit": "mg", "normal": 45.0, "warning": 250.0, "critical": 500.0, "current": 45.0},
            {"id": "DRAIN_PUMP_CURRENT", "name": "Sump Storm Pump Motor Amps", "param": "pump_current", "unit": "A", "normal": 32.0, "warning": 55.0, "critical": 80.0, "current": 32.0},
            {"id": "ROAD_SURFACE_RADAR", "name": "Vehicle Trapping Sensor", "param": "road_water_film", "unit": "mm", "normal": 0.0, "warning": 15.0, "critical": 50.0, "current": 0.0}
        ],
        "hazards": ["Sub-Surface Roadway Inundation", "Storm Drainage Pump Cavitation", "Flyover Resonance Overload", "Automated Traffic Diversion"],
        "default_risk": 10.0,
        "default_level": "NORMAL"
    },
    "INFRASTRUCTURE": {
        "id": "INFRASTRUCTURE",
        "name": "Narmada Valley Hydroelectric Dam & Spillway Intake",
        "type": "INFRASTRUCTURE",
        "location": "Sardar Sarovar Spillway Structure Block 7",
        "description": "Massive concrete gravity dam monitoring structural joint dilation and reservoir hydrostatic thrust.",
        "digital_twin_type": "DAM_SPILLWAY_SCADA",
        "camera_preset": {"pos": [-11.0, 9.0, 14.0], "target": [0, 2.0, 0]},
        "sensors": [
            {"id": "DAM_JOINT_LVDT", "name": "Spillway Joint Opening", "param": "joint_opening_mm", "unit": "mm", "normal": 1.8, "warning": 5.0, "critical": 9.0, "current": 1.8},
            {"id": "PIEZOMETER_PORE", "name": "Dam Foundation Pore Pressure", "param": "pore_pressure_kpa", "unit": "kPa", "normal": 165.0, "warning": 450.0, "critical": 750.0, "current": 165.0},
            {"id": "SEISMIC_STRONG_MOT", "name": "Crest Peak Ground Acceleration", "param": "crest_pga", "unit": "g", "normal": 0.02, "warning": 0.15, "critical": 0.35, "current": 0.02},
            {"id": "RESERVOIR_ULTRASONIC", "name": "Full Reservoir Level (FRL)", "param": "reservoir_level_m", "unit": "m", "normal": 138.6, "warning": 142.0, "critical": 144.5, "current": 138.6}
        ],
        "hazards": ["Spillway Monolith Joint Dilation", "Dam Foundation Uplift Surge", "Seismic Hydrodynamic Shear", "Spillway Sluice Gate Trip"],
        "default_risk": 14.0,
        "default_level": "NORMAL"
    },
    "REMOTE": {
        "id": "REMOTE",
        "name": "Ladakh High-Altitude Border Weather Observation Post",
        "type": "REMOTE",
        "location": "Chang La Pass 5,360m Elevation",
        "description": "Completely off-grid, sub-zero harsh weather research post operating on solar-battery reserve.",
        "digital_twin_type": "REMOTE_POST_SCADA",
        "camera_preset": {"pos": [-8.0, 6.0, 10.0], "target": [0, 1.0, 0]},
        "sensors": [
            {"id": "BLIZZARD_ANEMOMETER", "name": "Blizzard Gust Velocity", "param": "wind_gust_kmh", "unit": "km/h", "normal": 28.0, "warning": 80.0, "critical": 135.0, "current": 28.0},
            {"id": "CRYO_TEMP_RTD", "name": "Sub-Zero Cryo Ambient Temp", "param": "subzero_temp_c", "unit": "°C", "normal": -18.5, "warning": -35.0, "critical": -48.0, "current": -18.5},
            {"id": "BATTERY_SOC_BMS", "name": "Cold-Hardened LiFePO4 SoC", "param": "battery_soc", "unit": "%", "normal": 92.0, "warning": 35.0, "critical": 15.0, "current": 92.0},
            {"id": "SNOW_DEPTH_SONAR", "name": "Avalanche Snowpack Accumulation", "param": "snowpack_cm", "unit": "cm", "normal": 45.0, "warning": 160.0, "critical": 280.0, "current": 45.0}
        ],
        "hazards": ["Extreme Cryogenic Freeze (-45°C)", "Category 2 Blizzard Storm Gusts", "Critical Off-Grid Battery Depletion", "Avalanche Shelter Overburden"],
        "default_risk": 16.0,
        "default_level": "NORMAL"
    },
    "CUSTOM": {
        "id": "CUSTOM",
        "name": "User Facility — Photo-Reconstructed Room (Bed, TV, Window, Fan, Switchboard)",
        "type": "CUSTOM",
        "location": "Custom Reconstructed Site — 4-Photo Photogrammetric Digital Twin",
        "description": "High-fidelity digital twin reconstructed from room photographs: cot bed with mattress, wall-mounted LED TV, window with pleated drapes, modular power switchboard with relay trip, spinning 3-blade ceiling fan, and entrance security door.",
        "digital_twin_type": "PHOTO_RECONSTRUCTED_ROOM",
        "camera_preset": {"pos": [2.8, 1.8, 2.6], "target": [-0.6, 1.2, -0.4]},
        "sensors": [
            {"id": "ROOM_AMB_TEMP", "name": "Room Ambient Temp (PT100 Window Sensor)", "param": "motor_temperature", "unit": "°C", "normal": 25.4, "warning": 38.0, "critical": 52.0, "current": 25.4},
            {"id": "ROOM_VIBRATION", "name": "Ceiling Fan Structural Vibration (ADXL345)", "param": "bearing_vibration", "unit": "mm/s", "normal": 0.4, "warning": 2.2, "critical": 5.8, "current": 0.4},
            {"id": "SWITCHBOARD_LOAD_CURRENT", "name": "Switchboard Mains Circuit (ACS712)", "param": "motor_current", "unit": "A", "normal": 4.8, "warning": 12.0, "critical": 22.0, "current": 4.8},
            {"id": "TOF_OCCUPANCY", "name": "Bed Area Personnel Presence (VL53L1X)", "param": "worker_proximity", "unit": "m", "normal": 2.8, "warning": 1.2, "critical": 0.4, "current": 2.8}
        ],
        "hazards": ["Room Thermal Runaway / Overheating", "Ceiling Fan Bearing Vibration Imbalance", "Mains Switchboard Circuit Overcurrent", "Unauthorized Room Incursion"],
        "default_risk": 5.0,
        "default_level": "NORMAL"
    }
}

active_env_state = {
    "current_env": "INDUSTRIAL",
    "scenario": "NORMAL",
    "overrides": {}
}

@router.get("/active")
def get_active_environment_state():
    """Returns the full active environment metadata, active sensors, and digital twin scene config."""
    env_id = active_env_state["current_env"]
    meta = dict(ENV_METADATA.get(env_id, ENV_METADATA["INDUSTRIAL"]))
    
    # Apply scenario alterations if active
    scenario = active_env_state["scenario"]
    if scenario == "WARNING":
        meta["default_risk"] = 68.0
        meta["default_level"] = "WARNING"
        meta["sensors"][0]["current"] = meta["sensors"][0]["warning"] + 1.5
        meta["sensors"][1]["current"] = meta["sensors"][1]["warning"] + 0.5
    elif scenario == "CRITICAL":
        meta["default_risk"] = 96.0
        meta["default_level"] = "CRITICAL"
        meta["sensors"][0]["current"] = meta["sensors"][0]["critical"] + 2.0
        meta["sensors"][1]["current"] = meta["sensors"][1]["critical"] + 1.0
        if len(meta["sensors"]) > 3:
            meta["sensors"][3]["current"] = meta["sensors"][3].get("critical", 0.6)

    meta["active_scenario"] = scenario
    return meta

@router.get("/switch/{env_id}")
@router.post("/switch")
def switch_environment_profile(env_id: Optional[str] = None, body: Optional[Dict[str, Any]] = None):
    """Switches active deployment environment (INDUSTRIAL, INDOOR, NATURAL, URBAN, INFRASTRUCTURE, REMOTE, CUSTOM)."""
    target = env_id or (body.get("profile_id") if body else None) or "INDUSTRIAL"
    target_clean = target.upper()

    # Match aliases
    if "CUSTOM" in target_clean or "PHOTO" in target_clean or "ROOM" in target_clean:
        chosen = "CUSTOM"
    elif "INDUS" in target_clean:
        chosen = "INDUSTRIAL"
    elif "INDOOR" in target_clean:
        chosen = "INDOOR"
    elif "NATUR" in target_clean:
        chosen = "NATURAL"
    elif "URBAN" in target_clean:
        chosen = "URBAN"
    elif "INFRA" in target_clean or "DAM" in target_clean:
        chosen = "INFRASTRUCTURE"
    elif "REMOTE" in target_clean or "LADAKH" in target_clean:
        chosen = "REMOTE"
    else:
        chosen = "INDUSTRIAL"

    active_env_state["current_env"] = chosen
    active_env_state["scenario"] = "NORMAL"
    environment_registry.set_active_profile(chosen)

    env_data = get_active_environment_state()
    res = dict(env_data)
    res["status"] = "success"
    res["switched_to"] = chosen
    res["environment"] = env_data
    return res

@router.post("/scenario")
def set_environment_scenario(body: Dict[str, Any] = Body(...)):
    """Triggers scenario states (NORMAL, WARNING, CRITICAL) for the specified or current environment."""
    env_target = body.get("environment")
    if env_target:
        target_clean = str(env_target).upper()
        if "CUSTOM" in target_clean or "PHOTO" in target_clean or "ROOM" in target_clean:
            active_env_state["current_env"] = "CUSTOM"
        elif "INDOOR" in target_clean:
            active_env_state["current_env"] = "INDOOR"
        elif "NATUR" in target_clean:
            active_env_state["current_env"] = "NATURAL"
        elif "URBAN" in target_clean:
            active_env_state["current_env"] = "URBAN"
        elif "INFRA" in target_clean or "DAM" in target_clean:
            active_env_state["current_env"] = "INFRASTRUCTURE"
        elif "REMOTE" in target_clean or "LADAKH" in target_clean:
            active_env_state["current_env"] = "REMOTE"
        elif "INDUS" in target_clean:
            active_env_state["current_env"] = "INDUSTRIAL"

    scen = body.get("scenario", "NORMAL").upper()
    if scen not in ["NORMAL", "WARNING", "CRITICAL"]:
        scen = "NORMAL"
    active_env_state["scenario"] = scen

    env_data = get_active_environment_state()

    # Build telemetry state values matching active scenario
    telemetry_state = {}
    for s in env_data.get("sensors", []):
        param = s.get("param", s.get("id"))
        if scen == "NORMAL":
            telemetry_state[param] = s.get("normal", s.get("current", 0))
        elif scen == "WARNING":
            telemetry_state[param] = s.get("warning", s.get("normal", 0))
        else:
            telemetry_state[param] = s.get("critical", s.get("warning", 0))

    return {
        "status": "success",
        "scenario": scen,
        "environment": env_data,
        "id": env_data["id"],
        "name": env_data["name"],
        "risk_level": env_data["default_level"],
        "risk_score": env_data["default_risk"],
        "telemetry_state": telemetry_state,
        "actuators": {
            "motor_relay": scen != "CRITICAL",
            "beacon": "RED" if scen == "CRITICAL" else ("YELLOW" if scen == "WARNING" else "GREEN"),
            "siren_db": 95 if scen == "CRITICAL" else 0,
            "e_stop": scen == "CRITICAL"
        },
        "description": f"Scenario {scen} operational state applied to {env_data['name']}."
    }

