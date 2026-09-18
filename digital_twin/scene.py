"""
Sentinel-X Digital Twin: Industrial Scene Model & Object Mapping
================================================================
Defines 3D scene entities for the flagship industrial conveyor plant:
  - 45 kW AC Drive Motor (M007)
  - 2-Stage Helical Reduction Gearbox (GB-02)
  - Cylindrical Roller Bearings (B-101 Drive End, B-102 Non-Drive End)
  - 24m Industrial Heavy Rubberized Conveyor Belt (CV-01)
  - Head Discharge Pulley & Tail Take-up Pulley
  - Restricted Worker Pinch-Point Perimeter Zone
  - Emergency Pull-Wire Cable Interlock
  - 3-Stage Industrial Beacon Strobe & 110dB Acoustic Horn Tower
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SceneObject(BaseModel):
    object_id: str
    name: str
    category: str # MACHINE, STRUCTURE, SAFETY, SENSOR, ZONE
    dimensions_m: List[float] # [width, height, depth]
    position_m: List[float] # [x, y, z]
    material_finish: str = "WORN_CAST_IRON_RUST_PATINA"
    attached_sensor_id: Optional[str] = None
    telemetry_parameter: Optional[str] = None
    current_value: float = 0.0
    unit: str = ""
    status: str = "NOMINAL" # NOMINAL, WATCH, WARNING, CRITICAL, QUARANTINED
    highlight_color_hex: str = "#22C55E" # Green nominal

class IndustrialConveyorScene(BaseModel):
    facility_name: str = "Tata Heavy Raw Materials Sinter Plant — Unit 4"
    scene_type: str = "FLAGSHIP_CONVEYOR_3D_SCADA"
    wear_level: str = "MAINTAINED_LEGACY_HEAVY_INDUSTRY"
    objects: List[SceneObject] = Field(default_factory=list)

def get_flagship_industrial_scene() -> IndustrialConveyorScene:
    return IndustrialConveyorScene(
        objects=[
            SceneObject(
                object_id="OBJ_MOTOR_01",
                name="45kW 3-Phase Induction Drive Motor (M007)",
                category="MACHINE",
                dimensions_m=[1.2, 0.9, 0.9],
                position_m=[-4.5, 0.6, 0.0],
                material_finish="CHIPPED_GREEN_INDUSTRIAL_ENAMEL_SURFACE_OXIDATION",
                attached_sensor_id="PT100_MOTOR_TEMP",
                telemetry_parameter="motor_temperature",
                current_value=68.5,
                unit="°C",
                status="NOMINAL",
                highlight_color_hex="#22C55E"
            ),
            SceneObject(
                object_id="OBJ_GEARBOX_01",
                name="Helical Reduction Gearbox (GB-02 Ratio 1:28)",
                category="MACHINE",
                dimensions_m=[1.4, 1.1, 0.8],
                position_m=[-3.0, 0.7, 0.0],
                material_finish="HEAVY_CAST_IRON_GREASE_STAINED",
                attached_sensor_id="GEARBOX_TEMP",
                telemetry_parameter="gearbox_temperature",
                current_value=62.0,
                unit="°C",
                status="NOMINAL",
                highlight_color_hex="#22C55E"
            ),
            SceneObject(
                object_id="OBJ_BEARING_DRIVE",
                name="Drive Shaft Cylindrical Roller Bearing (B-101)",
                category="MACHINE",
                dimensions_m=[0.5, 0.5, 0.4],
                position_m=[-2.0, 0.5, 0.0],
                material_finish="MACHINED_STEEL_GREASE_ACCUMULATION",
                attached_sensor_id="ADXL345_VIBRATION",
                telemetry_parameter="bearing_vibration",
                current_value=2.4,
                unit="mm/s",
                status="NOMINAL",
                highlight_color_hex="#22C55E"
            ),
            SceneObject(
                object_id="OBJ_CONVEYOR_BELT",
                name="24-Meter Reinforced Rubberized Trough Belt",
                category="MACHINE",
                dimensions_m=[12.0, 0.3, 1.2],
                position_m=[2.0, 0.8, 0.0],
                material_finish="VULCANIZED_RUBBER_ORE_DUST_SCUFFED",
                attached_sensor_id="BELT_SPEED_ENCODER",
                telemetry_parameter="belt_speed",
                current_value=2.2,
                unit="m/s",
                status="NOMINAL",
                highlight_color_hex="#22C55E"
            ),
            SceneObject(
                object_id="OBJ_RESTRICTED_ZONE",
                name="Pinch-Point Danger Zone Optical Perimeter",
                category="ZONE",
                dimensions_m=[3.0, 2.0, 2.0],
                position_m=[-2.0, 0.0, 1.5],
                material_finish="YELLOW_BLACK_STRIPED_EPOXY_FLOOR_MARKING",
                attached_sensor_id="TOF_LIDAR_PROXIMITY",
                telemetry_parameter="worker_proximity",
                current_value=4.5,
                unit="meters",
                status="NOMINAL",
                highlight_color_hex="#3B82F6"
            ),
            SceneObject(
                object_id="OBJ_ESTOP_PULL_WIRE",
                name="Emergency Stop Tensioned Pull-Wire Circuit",
                category="SAFETY",
                dimensions_m=[12.0, 0.1, 0.1],
                position_m=[2.0, 0.6, 1.1],
                material_finish="RED_PVC_COATED_STEEL_CABLE",
                attached_sensor_id="ESTOP_PULL_WIRE",
                telemetry_parameter="estop_state",
                current_value=0.0,
                unit="binary",
                status="ARMED",
                highlight_color_hex="#22C55E"
            ),
            SceneObject(
                object_id="OBJ_BEACON_SIREN_TOWER",
                name="Industrial 3-Color Strobe Beacon & 110dB Acoustic Siren Tower",
                category="SAFETY",
                dimensions_m=[0.3, 1.8, 0.3],
                position_m=[-5.2, 1.2, 1.8],
                material_finish="GALVANIZED_STEEL_MOUNT_POLYCARBONATE_LENSES",
                attached_sensor_id=None,
                telemetry_parameter="beacon_state",
                current_value=1.0, # Green
                unit="state",
                status="GREEN_ACTIVE",
                highlight_color_hex="#22C55E"
            )
        ]
    )
