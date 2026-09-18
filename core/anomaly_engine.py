"""
Sentinel-X Core: Anomaly Detection Engine
=========================================
Environment-agnostic multi-parameter statistical and physics-based anomaly detector.
Detects:
  - Impossible rate-of-change jumps (physics violations)
  - Z-score statistical deviations from rolling baseline
  - Multi-sensor temporal drift
  - Frozen sensor states (stuck at exact float for prolonged time)
"""

import time
import math
from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel, Field

class AnomalyResult(BaseModel):
    sensor_id: str
    parameter: str
    is_anomaly: bool
    anomaly_score: float = Field(..., ge=0.0, le=1.0) # 0.0 = normal, 1.0 = severe anomaly
    anomaly_type: str # NONE, RATE_OF_CHANGE, OUT_OF_BOUNDS, STUCK_VALUE, DRIFT, CROSS_SENSOR_DISCREPANCY
    description: str
    timestamp: float = Field(default_factory=time.time)

class AnomalyEngine:
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.history: Dict[str, List[Tuple[float, float]]] = {} # sensor_id -> [(ts, value)]

    def record_reading(self, sensor_id: str, value: float, timestamp: Optional[float] = None):
        ts = timestamp or time.time()
        if sensor_id not in self.history:
            self.history[sensor_id] = []
        self.history[sensor_id].append((ts, value))
        if len(self.history[sensor_id]) > self.window_size:
            self.history[sensor_id].pop(0)

    def evaluate(self, sensor_id: str, value: float, max_rate_change: float = 15.0, 
                 min_limit: Optional[float] = None, max_limit: Optional[float] = None) -> AnomalyResult:
        self.record_reading(sensor_id, value)
        buf = self.history[sensor_id]

        # 1. Bounds Check
        if min_limit is not None and value < min_limit:
            return AnomalyResult(
                sensor_id=sensor_id, parameter="value", is_anomaly=True,
                anomaly_score=0.95, anomaly_type="OUT_OF_BOUNDS",
                description=f"Value {value} below physical lower limit {min_limit}"
            )
        if max_limit is not None and value > max_limit:
            return AnomalyResult(
                sensor_id=sensor_id, parameter="value", is_anomaly=True,
                anomaly_score=0.95, anomaly_type="OUT_OF_BOUNDS",
                description=f"Value {value} above physical upper limit {max_limit}"
            )

        # 2. Rate of Change Check
        if len(buf) >= 2:
            prev_ts, prev_val = buf[-2]
            curr_ts, curr_val = buf[-1]
            dt = max(0.01, curr_ts - prev_ts)
            rate = abs(curr_val - prev_val) / dt
            if rate > max_rate_change:
                return AnomalyResult(
                    sensor_id=sensor_id, parameter="value", is_anomaly=True,
                    anomaly_score=min(1.0, 0.5 + (rate / (2 * max_rate_change))),
                    anomaly_type="RATE_OF_CHANGE",
                    description=f"Rate of change {rate:.2f}/s exceeds max plausible {max_rate_change}/s"
                )

        # 3. Stuck Value Check (Sensor freeze/failure)
        if len(buf) >= 15:
            values = [v for _, v in buf[-15:]]
            if max(values) == min(values):
                return AnomalyResult(
                    sensor_id=sensor_id, parameter="value", is_anomaly=True,
                    anomaly_score=0.85, anomaly_type="STUCK_VALUE",
                    description="Sensor frozen: exact constant float value across 15 consecutive readings"
                )

        # 4. Statistical Z-Score
        if len(buf) >= 10:
            vals = [v for _, v in buf]
            mean = sum(vals) / len(vals)
            variance = sum((x - mean) ** 2 for x in vals) / len(vals)
            std = math.sqrt(variance)
            if std > 0.001:
                z = abs(value - mean) / std
                if z > 3.0:
                    score = min(1.0, 0.4 + (z * 0.15))
                    return AnomalyResult(
                        sensor_id=sensor_id, parameter="value", is_anomaly=True,
                        anomaly_score=score, anomaly_type="DRIFT",
                        description=f"Statistical anomaly: Z-score {z:.2f} standard deviations from mean"
                    )

        return AnomalyResult(
            sensor_id=sensor_id, parameter="value", is_anomaly=False,
            anomaly_score=0.05, anomaly_type="NONE",
            description="Nominal sensor behavior"
        )

anomaly_engine = AnomalyEngine()
