"""
Sentinel-X TinyML Kinematic Feature Extraction Pipeline
Extracts sliding-window statistical and kinematic features from river stage time-series.
Designed for low-memory execution on ESP32-S3 (Xtensa) and Raspberry Pi 5.
"""

import math
from typing import List, Dict, Any

class KinematicFeatureExtractor:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size

    def extract_features(self, stage_history: List[float], dt_seconds: float = 1.0) -> Dict[str, float]:
        """
        Extracts kinematic features from a sliding window of stage readings.
        """
        if len(stage_history) < 2:
            val = stage_history[0] if stage_history else 2.40
            return {
                "mean_stage_m": val,
                "variance_stage": 0.0,
                "rate_of_rise_m_min": 0.0,
                "acceleration_m_s2": 0.0,
                "kurtosis": 0.0,
                "spectral_energy": 0.0
            }

        window = stage_history[-self.window_size:]
        n = len(window)

        # 1. Mean & Variance
        mean_val = sum(window) / n
        var_val = sum((x - mean_val) ** 2 for x in window) / n

        # 2. Kinematic Rate of Rise (m / min)
        dt_min = (dt_seconds * (n - 1)) / 60.0
        rate_of_rise = (window[-1] - window[0]) / (dt_min if dt_min > 0 else 1.0 / 60.0)

        # 3. Kinematic Acceleration (Second derivative)
        accel = 0.0
        if n >= 3:
            v1 = (window[-1] - window[-2]) / dt_seconds
            v0 = (window[-2] - window[-3]) / dt_seconds
            accel = (v1 - v0) / dt_seconds

        # 4. Spectral Energy
        energy = sum(x ** 2 for x in window) / n

        return {
            "mean_stage_m": round(mean_val, 4),
            "variance_stage": round(var_val, 6),
            "rate_of_rise_m_min": round(rate_of_rise, 4),
            "acceleration_m_s2": round(accel, 6),
            "spectral_energy": round(energy, 4)
        }

feature_extractor = KinematicFeatureExtractor()
