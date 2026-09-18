"""
Synthetic Hydrological Dataset Generator
Produces physically constrained river stage time-series:
1. Normal Laminar Flow (Seasonal tidal oscillation)
2. Extreme Flash Flood Surge (Rapid step-ramp)
3. Sensor Spoofing Attack / Electrical Spike
"""

import math
from typing import List, Dict

def generate_laminar_stream(n_samples: int = 100, base_stage: float = 2.41) -> List[float]:
    stream = []
    for i in range(n_samples):
        val = base_stage + 0.04 * math.sin(i * 0.1) + 0.01 * math.cos(i * 0.25)
        stream.append(round(val, 3))
    return stream

def generate_flood_surge_stream(n_samples: int = 100, surge_start: int = 30) -> List[float]:
    stream = []
    curr = 2.41
    for i in range(n_samples):
        if i >= surge_start:
            curr += 0.05 # +0.05m per sample
        stream.append(round(curr, 3))
    return stream

def generate_spoofed_stream(n_samples: int = 100, spoof_at: int = 50, spike_val: float = 8.90) -> List[float]:
    stream = generate_laminar_stream(n_samples)
    if spoof_at < len(stream):
        stream[spoof_at] = spike_val
    return stream
