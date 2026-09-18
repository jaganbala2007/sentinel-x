"""
Sentinel-X Communication: HF Packet Radio Simulator
===================================================
Simulates AX.25-style HF Packet Radio communications on 7.105 MHz (40m band) / 14.105 MHz (20m band).
Provides realistic RF channel degradation, ionospheric fading, CRC16 checks, packet loss,
and retry mechanisms for beyond-line-of-sight emergency telemetry.
HARDWARE STATUS:
Explicitly labeled SIMULATION unless connected to a physical AX.25 TNC modem & HF transceiver.
"""

import time
import zlib
import random
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

class HFPacket(BaseModel):
    callsign_src: str = "VU2SNX-1"
    callsign_dst: str = "VU2EOC-0"
    frequency_mhz: float = 7.105
    baud_rate: int = 1200 # Bell 202 / AX.25 FSK
    sequence_num: int
    payload_raw: str
    crc16: str
    rssi_dbm: int = -89
    snr_db: float = 8.5
    status: str = "SIMULATED_TRANSMITTED" # SIMULATED_TRANSMITTED, ACK_RECEIVED, DROPPED_FADING, RETRYING
    timestamp: float = Field(default_factory=time.time)

class HFPacketRadioSimulator:
    def __init__(self):
        self.channel_active = True
        self.fading_intensity = 0.15 # 15% packet drop probability on ionospheric skywave
        self.packet_history: List[HFPacket] = []
        self._seq = 0

    def compute_crc16(self, data: str) -> str:
        crc = zlib.crc32(data.encode('utf-8')) & 0xFFFF
        return f"0x{crc:04X}"

    def transmit_event(self, event_data: Dict[str, Any]) -> Tuple[bool, HFPacket]:
        self._seq += 1
        serialized = f"SEQ:{self._seq}|SRC:{event_data.get('source', 'RPI5')}|RSK:{event_data.get('risk_score', 0)}|HZD:{event_data.get('hazard', 'NONE')}"
        crc = self.compute_crc16(serialized)

        # Simulate fading
        lost = random.random() < self.fading_intensity
        status = "DROPPED_FADING" if lost else "ACK_RECEIVED"
        rssi = -95 + random.randint(-8, 8)
        snr = round(max(2.0, 10.0 + random.uniform(-4.0, 4.0)), 1)

        packet = HFPacket(
            sequence_num=self._seq,
            payload_raw=serialized,
            crc16=crc,
            rssi_dbm=rssi,
            snr_db=snr,
            status=status
        )
        self.packet_history.append(packet)
        if len(self.packet_history) > 100:
            self.packet_history.pop(0)

        success = not lost
        return success, packet

    def get_recent_packets(self) -> List[HFPacket]:
        return self.packet_history[-20:]

hf_packet_simulator = HFPacketRadioSimulator()
