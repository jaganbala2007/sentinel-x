"""
Sentinel-X V2 Environment Manager Service
=========================================
Registry and state controller for Environment Profiles.
Manages active deployment environments (Natural, Indoor, Industrial, Infrastructure, Remote)
and generates environment-specific normalized sensor telemetry.
"""

from typing import Dict, List, Optional
import time
from app.schemas.universal import (
    EnvironmentProfile,
    EnvironmentType,
    HazardType,
    SensorDefinition,
    NormalizedSensorReading,
    LocationModel
)

class EnvironmentManager:
    def __init__(self):
        self.profiles: Dict[EnvironmentType, EnvironmentProfile] = self._init_profiles()
        self.active_profile_id: EnvironmentType = EnvironmentType.NATURAL_OUTDOOR

    def _init_profiles(self) -> Dict[EnvironmentType, EnvironmentProfile]:
        # 1. Natural Outdoor (Hero SIH Environment)
        natural = EnvironmentProfile(
            id=EnvironmentType.NATURAL_OUTDOOR,
            name="Natural Watershed / River Basin",
            description="Outdoor river basin, floodplains, reservoirs, and mountain hydrology monitoring.",
            active_hazards=[HazardType.FLASH_FLOOD, HazardType.FLOOD, HazardType.LANDSLIDE, HazardType.POWER_FAILURE],
            sensor_definitions=[
                SensorDefinition(
                    sensor_type="ultrasonic_depth",
                    metric_name="water_level_m",
                    unit="m",
                    min_plausible=0.0,
                    max_plausible=12.0,
                    max_rate_of_change=0.40,
                    warning_threshold=3.20,
                    critical_threshold=3.50,
                    is_primary=True
                ),
                SensorDefinition(
                    sensor_type="barometric_pressure",
                    metric_name="baro_pressure_hpa",
                    unit="hPa",
                    min_plausible=850.0,
                    max_plausible=1080.0,
                    max_rate_of_change=5.0,
                    warning_threshold=990.0,
                    critical_threshold=975.0
                ),
                SensorDefinition(
                    sensor_type="ambient_temperature",
                    metric_name="temperature_c",
                    unit="°C",
                    min_plausible=-10.0,
                    max_plausible=55.0,
                    max_rate_of_change=5.0,
                    warning_threshold=38.0,
                    critical_threshold=45.0
                )
            ],
            communication_priority=["INTERNET", "HF_PACKET", "SATELLITE", "OFFLINE"],
            spatial_reference="GEOGRAPHIC_GIS",
            primary_response_actions=["ACTIVATE_LOCAL_SIREN", "DISPATCH_EVACUATION_ALERT", "BUFFER_OFFLINE"],
            autonomous_siren_enabled=True
        )

        # 2. Indoor Building (High-Rise / Campus / Warehouse)
        indoor = EnvironmentProfile(
            id=EnvironmentType.INDOOR_BUILDING,
            name="Commercial & Institutional High-Rise",
            description="Multi-story structures, data centers, hospitals, and educational facilities.",
            active_hazards=[HazardType.FIRE, HazardType.SMOKE, HazardType.GAS_LEAK, HazardType.POWER_FAILURE],
            sensor_definitions=[
                SensorDefinition(
                    sensor_type="optical_smoke",
                    metric_name="smoke_obscuration_pct_m",
                    unit="%/m",
                    min_plausible=0.0,
                    max_plausible=20.0,
                    max_rate_of_change=2.0,
                    warning_threshold=1.5,
                    critical_threshold=4.0,
                    is_primary=True
                ),
                SensorDefinition(
                    sensor_type="ambient_temperature",
                    metric_name="temperature_c",
                    unit="°C",
                    min_plausible=5.0,
                    max_plausible=120.0,
                    max_rate_of_change=10.0,
                    warning_threshold=45.0,
                    critical_threshold=65.0
                ),
                SensorDefinition(
                    sensor_type="co_gas_detector",
                    metric_name="co_ppm",
                    unit="ppm",
                    min_plausible=0.0,
                    max_plausible=1000.0,
                    max_rate_of_change=50.0,
                    warning_threshold=25.0,
                    critical_threshold=50.0
                )
            ],
            communication_priority=["INTERNET", "ETHERNET", "WIFI", "OFFLINE"],
            spatial_reference="TOPOLOGICAL_BUILDING",
            primary_response_actions=["TRIGGER_FIRE_ALARM", "ACTIVATE_STAIRWELL_PRESSURIZATION", "NOTIFY_EOC"],
            autonomous_siren_enabled=True
        )

        # 3. Industrial Plant / Chemical Facility
        industrial = EnvironmentProfile(
            id=EnvironmentType.INDUSTRIAL,
            name="Industrial Chemical & Process Facility",
            description="Refineries, manufacturing bays, chemical synthesis lines, and process utilities.",
            active_hazards=[HazardType.GAS_LEAK, HazardType.FIRE, HazardType.EQUIPMENT_FAILURE, HazardType.POWER_FAILURE],
            sensor_definitions=[
                SensorDefinition(
                    sensor_type="catalytic_combustible_gas",
                    metric_name="gas_concentration_ppm",
                    unit="ppm",
                    min_plausible=0.0,
                    max_plausible=5000.0,
                    max_rate_of_change=200.0,
                    warning_threshold=50.0,
                    critical_threshold=100.0,
                    is_primary=True
                ),
                SensorDefinition(
                    sensor_type="piezo_vibration",
                    metric_name="vibration_mm_s",
                    unit="mm/s",
                    min_plausible=0.0,
                    max_plausible=50.0,
                    max_rate_of_change=10.0,
                    warning_threshold=4.5,
                    critical_threshold=7.5
                ),
                SensorDefinition(
                    sensor_type="manifold_pressure",
                    metric_name="manifold_pressure_bar",
                    unit="bar",
                    min_plausible=0.0,
                    max_plausible=30.0,
                    max_rate_of_change=5.0,
                    warning_threshold=18.0,
                    critical_threshold=22.0
                )
            ],
            communication_priority=["ETHERNET_MODBUS", "INTERNET", "HF_PACKET", "OFFLINE"],
            spatial_reference="TOPOLOGICAL_BUILDING",
            primary_response_actions=["ISOLATE_PROCESS_VALVES", "TRIGGER_EXHAUST_FANS", "PLANT_EVACUATION"],
            autonomous_siren_enabled=True
        )

        # 4. Critical Infrastructure (Bridges / Dams / Tunnels)
        infrastructure = EnvironmentProfile(
            id=EnvironmentType.CRITICAL_INFRASTRUCTURE,
            name="Civil Infrastructure (Bridge / Dam / Viaduct)",
            description="Highway spans, structural piers, tunnel portals, and reservoir retaining walls.",
            active_hazards=[HazardType.STRUCTURAL_ANOMALY, HazardType.FLOOD, HazardType.POWER_FAILURE],
            sensor_definitions=[
                SensorDefinition(
                    sensor_type="triaxial_accelerometer",
                    metric_name="vibration_mm_s",
                    unit="mm/s",
                    min_plausible=0.0,
                    max_plausible=40.0,
                    max_rate_of_change=8.0,
                    warning_threshold=4.0,
                    critical_threshold=7.5,
                    is_primary=True
                ),
                SensorDefinition(
                    sensor_type="digital_inclinometer",
                    metric_name="tilt_deg",
                    unit="°",
                    min_plausible=-10.0,
                    max_plausible=10.0,
                    max_rate_of_change=1.0,
                    warning_threshold=0.8,
                    critical_threshold=2.0
                ),
                SensorDefinition(
                    sensor_type="reservoir_depth",
                    metric_name="water_level_m",
                    unit="m",
                    min_plausible=0.0,
                    max_plausible=25.0,
                    max_rate_of_change=0.50,
                    warning_threshold=18.0,
                    critical_threshold=21.0
                )
            ],
            communication_priority=["INTERNET", "SATELLITE", "HF_PACKET", "OFFLINE"],
            spatial_reference="GEOGRAPHIC_GIS",
            primary_response_actions=["ACTIVATE_LOAD_RESTRICTIONS", "TRIGGER_STRUCTURAL_ALARM", "NOTIFY_DOT"],
            autonomous_siren_enabled=True
        )

        # 5. Remote Disaster Zone
        remote = EnvironmentProfile(
            id=EnvironmentType.REMOTE_DISASTER_ZONE,
            name="Remote Disaster Zone / Low-Bandwidth",
            description="Isolated mountain valleys, storm-damaged sectors with zero grid or cellular infrastructure.",
            active_hazards=[HazardType.FLASH_FLOOD, HazardType.LANDSLIDE, HazardType.POWER_FAILURE],
            sensor_definitions=[
                SensorDefinition(
                    sensor_type="ultrasonic_depth",
                    metric_name="water_level_m",
                    unit="m",
                    min_plausible=0.0,
                    max_plausible=15.0,
                    max_rate_of_change=0.50,
                    warning_threshold=3.0,
                    critical_threshold=3.50,
                    is_primary=True
                ),
                SensorDefinition(
                    sensor_type="ground_vibration",
                    metric_name="vibration_mm_s",
                    unit="mm/s",
                    min_plausible=0.0,
                    max_plausible=30.0,
                    max_rate_of_change=5.0,
                    warning_threshold=3.5,
                    critical_threshold=6.0
                )
            ],
            communication_priority=["HF_PACKET", "SATELLITE", "OFFLINE"],
            spatial_reference="GEOGRAPHIC_GIS",
            primary_response_actions=["LOCAL_SIREN_ONLY", "HF_EMERGENCY_BROADCAST", "STORE_AND_FORWARD"],
            autonomous_siren_enabled=True
        )

        return {
            EnvironmentType.NATURAL_OUTDOOR: natural,
            EnvironmentType.INDOOR_BUILDING: indoor,
            EnvironmentType.INDUSTRIAL: industrial,
            EnvironmentType.CRITICAL_INFRASTRUCTURE: infrastructure,
            EnvironmentType.REMOTE_DISASTER_ZONE: remote
        }

    def get_active_profile(self) -> EnvironmentProfile:
        return self.profiles[self.active_profile_id]

    def get_all_profiles(self) -> List[EnvironmentProfile]:
        return list(self.profiles.values())

    def switch_profile(self, profile_id: EnvironmentType) -> EnvironmentProfile:
        if profile_id in self.profiles:
            self.active_profile_id = profile_id
        return self.get_active_profile()

    def generate_baseline_readings(self) -> List[NormalizedSensorReading]:
        """Generate baseline operational readings conforming to the active profile."""
        profile = self.get_active_profile()
        now_ms = int(time.time() * 1000)
        readings = []

        if profile.id == EnvironmentType.NATURAL_OUTDOOR:
            nodes = [
                ("NODE-01", 2.42, LocationModel(latitude=27.054, longitude=88.542, elevation_m=280.0)),
                ("NODE-02", 2.38, LocationModel(latitude=27.061, longitude=88.548, elevation_m=275.0)),
                ("NODE-03", 2.45, LocationModel(latitude=27.048, longitude=88.539, elevation_m=285.0)),
            ]
            for nid, val, loc in nodes:
                readings.append(NormalizedSensorReading(
                    reading_id=f"{nid}-WAT-{now_ms}",
                    node_id=nid,
                    sensor_type="ultrasonic_depth",
                    metric_name="water_level_m",
                    value=val,
                    unit="m",
                    location=loc,
                    battery_pct=94,
                    auxiliary_metrics={"rate_of_rise_m_min": 0.01, "baro_pressure_hpa": 1013.2}
                ))

        elif profile.id == EnvironmentType.INDOOR_BUILDING:
            nodes = [
                ("NODE-01", 0.2, 23.5, LocationModel(building_id="BLDG-A", floor_level=3, room_or_zone="SERVER-ROOM")),
                ("NODE-02", 0.1, 24.1, LocationModel(building_id="BLDG-A", floor_level=4, room_or_zone="LAB-02")),
                ("NODE-03", 0.3, 23.8, LocationModel(building_id="BLDG-A", floor_level=2, room_or_zone="ATRIUM")),
            ]
            for nid, smoke, temp, loc in nodes:
                readings.append(NormalizedSensorReading(
                    reading_id=f"{nid}-SMK-{now_ms}",
                    node_id=nid,
                    sensor_type="optical_smoke",
                    metric_name="smoke_obscuration_pct_m",
                    value=smoke,
                    unit="%/m",
                    location=loc,
                    battery_pct=98,
                    auxiliary_metrics={"temperature_c": temp, "co_ppm": 2.0}
                ))

        elif profile.id == EnvironmentType.INDUSTRIAL:
            nodes = [
                ("NODE-01", 8.5, 1.2, LocationModel(building_id="PLANT-01", room_or_zone="MANIFOLD-BAY-1")),
                ("NODE-02", 9.1, 1.4, LocationModel(building_id="PLANT-01", room_or_zone="COMPRESSOR-ROOM")),
                ("NODE-03", 7.8, 1.1, LocationModel(building_id="PLANT-01", room_or_zone="STORAGE-TANK-4")),
            ]
            for nid, gas, vib, loc in nodes:
                readings.append(NormalizedSensorReading(
                    reading_id=f"{nid}-GAS-{now_ms}",
                    node_id=nid,
                    sensor_type="catalytic_combustible_gas",
                    metric_name="gas_concentration_ppm",
                    value=gas,
                    unit="ppm",
                    location=loc,
                    battery_pct=92,
                    auxiliary_metrics={"vibration_mm_s": vib, "manifold_pressure_bar": 12.5}
                ))

        elif profile.id == EnvironmentType.CRITICAL_INFRASTRUCTURE:
            nodes = [
                ("NODE-01", 1.15, 0.12, LocationModel(latitude=27.102, longitude=88.511, elevation_m=110.0)),
                ("NODE-02", 1.20, 0.10, LocationModel(latitude=27.105, longitude=88.515, elevation_m=110.0)),
                ("NODE-03", 1.18, 0.14, LocationModel(latitude=27.108, longitude=88.519, elevation_m=110.0)),
            ]
            for nid, vib, tilt, loc in nodes:
                readings.append(NormalizedSensorReading(
                    reading_id=f"{nid}-VIB-{now_ms}",
                    node_id=nid,
                    sensor_type="triaxial_accelerometer",
                    metric_name="vibration_mm_s",
                    value=vib,
                    unit="mm/s",
                    location=loc,
                    battery_pct=89,
                    auxiliary_metrics={"tilt_deg": tilt}
                ))

        else: # REMOTE_DISASTER_ZONE
            nodes = [
                ("NODE-01", 2.45, LocationModel(latitude=27.150, longitude=88.600, elevation_m=620.0)),
                ("NODE-02", 2.40, LocationModel(latitude=27.155, longitude=88.605, elevation_m=615.0)),
            ]
            for nid, val, loc in nodes:
                readings.append(NormalizedSensorReading(
                    reading_id=f"{nid}-WAT-{now_ms}",
                    node_id=nid,
                    sensor_type="ultrasonic_depth",
                    metric_name="water_level_m",
                    value=val,
                    unit="m",
                    location=loc,
                    battery_pct=82,
                    auxiliary_metrics={"vibration_mm_s": 0.8}
                ))

        return readings

environment_manager = EnvironmentManager()
