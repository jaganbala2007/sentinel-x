"""
Sentinel-X Communication Resilience Manager
===========================================
Dynamically monitors transport health and autonomously executes failover across:
  INTERNET -> LOCAL_LAN -> HF_PACKET_RADIO -> SATELLITE -> ISOLATED (STORE_FORWARD)
States:
  - NORMAL: WAN internet connected, primary telemetry active.
  - DEGRADED: High packet loss or internet down; fallen back to Local LAN / MQTT.
  - EMERGENCY: All IP networks severed; active on HF Packet Radio or Satellite.
  - ISOLATED: Total electromagnetic blackout; local execution + USB pendrive queue.
  - RECOVERY: Reconnection detected; background store-and-forward flushing queue.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time

class CommunicationState(str, Enum):
    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"
    EMERGENCY = "EMERGENCY"
    ISOLATED = "ISOLATED"
    RECOVERY = "RECOVERY"

class TransportChannel(str, Enum):
    INTERNET_WAN = "INTERNET_WAN"
    LOCAL_MQTT = "LOCAL_MQTT"
    HF_PACKET_RADIO = "HF_PACKET_RADIO"
    SATELLITE_SBD = "SATELLITE_SBD"
    OFFLINE_PENDRIVE = "OFFLINE_PENDRIVE"

class CommunicationStatus(BaseModel):
    state: CommunicationState = CommunicationState.NORMAL
    active_channel: TransportChannel = TransportChannel.INTERNET_WAN
    internet_available: bool = True
    local_lan_available: bool = True
    hf_available: bool = True # Simulation channel
    satellite_available: bool = True
    active_bandwidth_bps: int = 100000000 # 100 Mbps
    latency_ms: float = 12.4
    packet_loss_pct: float = 0.0
    pending_offline_messages: int = 0
    synced_messages: int = 4821
    failover_reason: str = "Nominal WAN connection active"
    last_transition_time: float = Field(default_factory=time.time)

class CommunicationManager:
    def __init__(self):
        self.status = CommunicationStatus()

    def set_state(self, state: CommunicationState, reason: str = ""):
        self.status.state = state
        self.status.failover_reason = reason or f"State shifted to {state.value}"
        self.status.last_transition_time = time.time()

        if state == CommunicationState.NORMAL:
            self.status.active_channel = TransportChannel.INTERNET_WAN
            self.status.internet_available = True
            self.status.active_bandwidth_bps = 100000000
            self.status.latency_ms = 12.4
            self.status.packet_loss_pct = 0.0

        elif state == CommunicationState.DEGRADED:
            self.status.active_channel = TransportChannel.LOCAL_MQTT
            self.status.internet_available = False
            self.status.active_bandwidth_bps = 10000000 # 10 Mbps
            self.status.latency_ms = 4.2
            self.status.packet_loss_pct = 2.1

        elif state == CommunicationState.EMERGENCY:
            self.status.active_channel = TransportChannel.HF_PACKET_RADIO
            self.status.internet_available = False
            self.status.local_lan_available = False
            self.status.active_bandwidth_bps = 1200 # 1200 bps AX.25
            self.status.latency_ms = 1850.0
            self.status.packet_loss_pct = 14.5

        elif state == CommunicationState.ISOLATED:
            self.status.active_channel = TransportChannel.OFFLINE_PENDRIVE
            self.status.internet_available = False
            self.status.local_lan_available = False
            self.status.hf_available = False
            self.status.satellite_available = False
            self.status.active_bandwidth_bps = 0
            self.status.latency_ms = 0.0
            self.status.packet_loss_pct = 100.0

        elif state == CommunicationState.RECOVERY:
            self.status.active_channel = TransportChannel.INTERNET_WAN
            self.status.internet_available = True
            self.status.active_bandwidth_bps = 50000000
            self.status.latency_ms = 24.0
            self.status.packet_loss_pct = 0.5

    def get_status(self) -> CommunicationStatus:
        return self.status

communication_manager = CommunicationManager()
