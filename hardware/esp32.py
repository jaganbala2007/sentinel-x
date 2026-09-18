"""
Sentinel-X Hardware Abstraction: ESP32-S3 Distributed Sensing Node
===================================================================
Represents field sensing microcontrollers running FreeRTOS.
Strictly requires labeling every sensor reading:
  - LIVE (physical hardware connected and verified)
  - SIMULATED
  - INFERRED
  - OFFLINE
  - PLANNED
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ESP32NodeStatus(BaseModel):
    node_id: str
    mac_address: str
    firmware_version: str = "v2.5.0-FreeRTOS"
    cpu_freq_mhz: int = 240
    battery_pct: int = 96
    rssi_dbm: int = -64
    free_heap_bytes: int = 284160
    temperature_internal_c: float = 38.5
    sensor_health: str = "HEALTHY" # HEALTHY, DEGRADED, FAULTY
    last_heartbeat_s_ago: float = 0.4
    data_source: str = "SIMULATED" # LIVE, SIMULATED, INFERRED, OFFLINE, PLANNED
    attached_sensors: List[str] = Field(default_factory=list)

class ESP32FleetManager:
    def __init__(self):
        self.nodes: Dict[str, ESP32NodeStatus] = {
            "ESP32-NODE-01": ESP32NodeStatus(
                node_id="ESP32-NODE-01",
                mac_address="34:85:18:9A:E2:01",
                battery_pct=98,
                rssi_dbm=-62,
                sensor_health="HEALTHY",
                data_source="SIMULATED",
                attached_sensors=["PT100_MOTOR_TEMP", "ADXL345_VIBRATION", "ACS712_CURRENT"]
            ),
            "ESP32-NODE-02": ESP32NodeStatus(
                node_id="ESP32-NODE-02",
                mac_address="34:85:18:9A:E2:02",
                battery_pct=94,
                rssi_dbm=-68,
                sensor_health="HEALTHY",
                data_source="SIMULATED",
                attached_sensors=["GEARBOX_TEMP", "ROLLER_BEARING_VIB", "BELT_SPEED_ENCODER"]
            ),
            "ESP32-NODE-03": ESP32NodeStatus(
                node_id="ESP32-NODE-03",
                mac_address="34:85:18:9A:E2:03",
                battery_pct=96,
                rssi_dbm=-65,
                sensor_health="HEALTHY",
                data_source="SIMULATED",
                attached_sensors=["TOF_LIDAR_PROXIMITY", "ESTOP_PULL_WIRE", "MQ135_GAS_SMOKE"]
            ),
            "ESP32-NODE-04": ESP32NodeStatus(
                node_id="ESP32-NODE-04",
                mac_address="34:85:18:9A:E2:04",
                battery_pct=91,
                rssi_dbm=-71,
                sensor_health="HEALTHY",
                data_source="SIMULATED",
                attached_sensors=["3PHASE_VOLTAGE", "AMBIENT_BME280"]
            )
        }

    def get_all_nodes(self) -> List[ESP32NodeStatus]:
        return list(self.nodes.values())

    def update_node_status(self, node_id: str, **kwargs):
        if node_id in self.nodes:
            for k, v in kwargs.items():
                if hasattr(self.nodes[node_id], k):
                    setattr(self.nodes[node_id], k, v)

esp32_fleet_manager = ESP32FleetManager()
