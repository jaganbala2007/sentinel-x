"""
Sentinel-X Communication: Satellite Adapter
===========================================
Simulates low-earth-orbit (LEO) Short Burst Data (SBD) emergency telemetry (Iridium 9603 / RockBLOCK).
HARDWARE STATUS:
Explicitly labeled SIMULATION unless connected to a physical serial satellite transceiver modem.
"""

import time
import random
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SatelliteSBDMessage(BaseModel):
    momsn: int # Mobile Originated Message Sequence Number
    imei: str = "300234063901230"
    constellation: str = "IRIDIUM_LEO"
    signal_bars: int = Field(default=4, ge=0, le=5)
    payload_hex: str
    status: str = "DELIVERED_GATEWAY"
    latency_seconds: float = 18.2
    timestamp: float = Field(default_factory=time.time)

class SatelliteAdapter:
    def __init__(self):
        self.signal_strength = 4
        self.momsn_counter = 100
        self.sent_messages: List[SatelliteSBDMessage] = []

    def transmit_burst(self, event_data: Dict[str, Any]) -> SatelliteSBDMessage:
        self.momsn_counter += 1
        raw_text = f"{event_data.get('event_id', 'EVT')}:{event_data.get('hazard', 'NONE')}:{event_data.get('risk_score', 0)}"
        hex_data = raw_text.encode('utf-8').hex().upper()

        msg = SatelliteSBDMessage(
            momsn=self.momsn_counter,
            payload_hex=hex_data,
            signal_bars=self.signal_strength,
            status="DELIVERED_GATEWAY",
            latency_seconds=round(random.uniform(12.0, 28.0), 1)
        )
        self.sent_messages.append(msg)
        return msg

    def get_recent_messages(self) -> List[SatelliteSBDMessage]:
        return self.sent_messages[-20:]

satellite_adapter = SatelliteAdapter()
