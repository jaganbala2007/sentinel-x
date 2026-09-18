"""
Sentinel-X Communication Resilience Package
============================================
Adaptive failover communication channels:
  1. Internet (TLS / REST / WebSocket)
  2. Local Network (mDNS / Local MQTT)
  3. HF Packet Radio Simulator (7.105 MHz AX.25 protocol)
  4. Satellite Adapter (Iridium SBD simulation)
  5. Store-and-Forward (Resilient offline queuing via USB pendrive)
"""

from communication.manager import communication_manager, CommunicationState, CommunicationStatus
from communication.mqtt_adapter import mqtt_adapter
from communication.hf_simulator import hf_packet_simulator
from communication.satellite_adapter import satellite_adapter
from communication.store_forward import store_and_forward_manager

__all__ = [
    "communication_manager",
    "CommunicationState",
    "CommunicationStatus",
    "mqtt_adapter",
    "hf_packet_simulator",
    "satellite_adapter",
    "store_and_forward_manager",
]
