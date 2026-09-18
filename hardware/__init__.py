"""
Sentinel-X Hardware Abstraction Layer
=====================================
Modular abstractions for:
  - Raspberry Pi 5 (Primary Edge Intelligence Unit)
  - USB Pendrive (Secondary Resilient Data Store)
  - ESP32-S3 (Distributed Sensing Node Fleet)
  - Actuators & Interlocks (E-Stop, Motor Relay, 3-Color Beacon, 110dB Siren)
"""

from hardware.raspberry_pi import raspberry_pi_manager, RPi5Metrics
from hardware.pendrive import usb_pendrive_store, PendriveMetrics, ResilientStorage
from hardware.esp32 import esp32_fleet_manager, ESP32NodeStatus
from hardware.actuators import actuator_manager, ActuatorState
from hardware.power_manager import power_manager, PowerMetrics

__all__ = [
    "raspberry_pi_manager",
    "RPi5Metrics",
    "usb_pendrive_store",
    "PendriveMetrics",
    "ResilientStorage",
    "esp32_fleet_manager",
    "ESP32NodeStatus",
    "actuator_manager",
    "ActuatorState",
    "power_manager",
    "PowerMetrics",
]
