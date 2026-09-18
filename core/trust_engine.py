# Copied from backend/app/core/trust_engine.py
"""
Sentinel-X Sensor Trust & Data Integrity Engine
===============================================
Evaluates sensor reliability, detects cross-sensor inconsistencies, enforces physical
plausibility rules, tracks data provenance, and computes weighted sensor consensus.
"""

import time
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

class DataProvenance(BaseModel):
    source: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str
    sequence_id: int
    trust_score: float = Field(..., ge=0.0, le=100.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    status: str = "TRUSTED"  # TRUSTED, UNTRUSTED, ESTIMATED, SIMULATED, STALE, OFFLINE

class SensorObservation(BaseModel):
    parameter: str
    value: float
    unit: str
    source: str
    device_id: str
    timestamp: float = Field(default_factory=time.time)
    provenance: Optional[DataProvenance] = None

class TrustEngine:
    def __init__(self):
        # Baseline device trust scores (0-100)
        self.device_trust_registry: Dict[str, float] = {
            "THERMAL_CAM_01": 97.0,
            "THERMAL_CAM_02": 96.5,
            "SENSOR_TEMP_AUX_B": 92.0,
            "SENSOR_TEMP_AUX_A": 91.0,
            "PLC_TEMP_M007": 94.0,
            "PLC_VIB_M007": 95.0,
            "PLC_CURRENT_M007": 93.0,
            "PLC_RPM_M007": 96.0,
            "ENV_GAS_ZONA": 95.0,
            "ENV_GAS_ZONB": 94.0,
        }
        # Historical buffer for temporal consistency checks: device_id -> List of (timestamp, value)
        self.history: Dict[str, List[Tuple[float, float]]] = {}
        # Degradation event log
        self.trust_events: List[Dict[str, Any]] = []

    def record_reading(self, device_id: str, value: float, timestamp: Optional[float] = None) -> None:
        """Stores reading in short-term history buffer."""
        ts = timestamp or time.time()
        if device_id not in self.history:
            self.history[device_id] = []
        self.history[device_id].append((ts, value))
        # Keep last 60 readings
        if len(self.history[device_id]) > 60:
            self.history[device_id].pop(0)

    def check_temporal_consistency(self, device_id: str, new_value: float, max_jump_per_sec: float = 15.0, timestamp: Optional[float] = None) -> Tuple[bool, str]:
        """
        Detects impossible rate-of-change jumps (e.g. temperature dropping 40°C in 1 second).
        """
        if device_id not in self.history or not self.history[device_id]:
            return True, "Baseline recorded"

        last_ts, last_val = self.history[device_id][-1]
        now_ts = timestamp or time.time()
        dt = max(1.0, now_ts - last_ts)
        rate_of_change = abs(new_value - last_val) / dt

        if rate_of_change > max_jump_per_sec:
            return False, f"Impossible rate of change: {rate_of_change:.1f} units/sec exceeds physical limit of {max_jump_per_sec} units/sec"
        return True, "Rate of change physically plausible"

    def check_physical_plausibility(self, parameters: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Validates multi-variable physics constraints across related parameters.
        Examples:
          - High current + high vibration cannot occur with cold/low temperature in active machine.
          - Machine state OFF cannot report RPM > 50.
          - Negative pressure or temperature below absolute zero.
        """
        warnings = []
        is_plausible = True

        temp = parameters.get("temperature")
        current = parameters.get("current")
        vibration = parameters.get("vibration")
        rpm = parameters.get("rpm")
        power_state = parameters.get("power_state", 1.0)

        # Rule 1: High current & vibration but reported temperature is unexpectedly low
        if current is not None and vibration is not None and temp is not None:
            if current > 45.0 and vibration > 7.0 and temp < 50.0:
                is_plausible = False
                warnings.append(
                    "Physical Inconsistency: High motor current (%.1f A) and severe vibration (%.1f mm/s) "
                    "conflicts with reported cold temperature (%.1f°C)." % (current, vibration, temp)
                )

        # Rule 2: Machine OFF but high RPM reported
        if power_state == 0.0 and rpm is not None and rpm > 50.0:
            is_plausible = False
            warnings.append(f"Physical Inconsistency: Machine is powered OFF but RPM is reporting {rpm:.0f} RPM.")

        # Rule 3: Extreme non-physical bounds
        if temp is not None and (temp < -40.0 or temp > 500.0):
            is_plausible = False
            warnings.append(f"Sensor Out-of-Bounds: Reported temperature {temp:.1f}°C violates physical plant limits.")

        return is_plausible, warnings

    def evaluate_sensor_consensus(
        self,
        parameter_name: str,
        observations: List[SensorObservation],
        outlier_threshold_sigma: float = 2.0
    ) -> Dict[str, Any]:
        """
        Computes robust weighted sensor consensus using source trust scores and outlier detection.
        Returns:
          - trusted_value: consensus value
          - consensus_confidence: 0.0 - 1.0
          - consensus_status: TRUSTED | CONFLICT_DETECTED | UNTRUSTED
          - validated_sources: breakdown of trust and consistency per source
        """
        if not observations:
            return {
                "parameter": parameter_name,
                "trusted_value": 0.0,
                "confidence": 0.0,
                "status": "OFFLINE",
                "sources": [],
                "warnings": ["No active sensor observations available"]
            }

        if len(observations) == 1:
            obs = observations[0]
            t_score = self.device_trust_registry.get(obs.device_id, 80.0)
            return {
                "parameter": parameter_name,
                "trusted_value": obs.value,
                "confidence": t_score / 100.0,
                "status": "TRUSTED" if t_score > 70 else "UNTRUSTED",
                "sources": [{
                    "device_id": obs.device_id,
                    "source": obs.source,
                    "value": obs.value,
                    "trust_score": t_score,
                    "status": "SINGLE_SOURCE"
                }],
                "warnings": ["Single sensor source - redundant validation unavailable"]
            }

        total_weight = 0.0
        weighted_sum = 0.0
        source_evals = []
        for obs in observations:
            base_trust = self.device_trust_registry.get(obs.device_id, 85.0)
            weight = max(0.01, base_trust / 100.0)
            total_weight += weight
            weighted_sum += obs.value * weight

        raw_weighted_mean = weighted_sum / total_weight

        conflicts = []
        valid_weighted_sum = 0.0
        valid_weight = 0.0

        for obs in observations:
            base_trust = self.device_trust_registry.get(obs.device_id, 85.0)
            deviation = abs(obs.value - raw_weighted_mean)
            other_vals = [o.value for o in observations if o.device_id != obs.device_id]
            median_others = sorted(other_vals)[len(other_vals)//2] if other_vals else raw_weighted_mean
            is_outlier = abs(obs.value - median_others) > 20.0

            if is_outlier:
                current_trust = max(20.0, base_trust * 0.4)
                self.device_trust_registry[obs.device_id] = round(current_trust, 1)
                conflicts.append(
                    f"Inconsistency Detected: {obs.source} ({obs.device_id}) reported {obs.value:.1f}{obs.unit} "
                    f"conflicts with independent consensus ~{median_others:.1f}{obs.unit} (trust degraded to {current_trust:.1f}%)"
                )
                source_status = "CONFLICT_ANOMALOUS"
            else:
                current_trust = min(100.0, base_trust + 0.5)
                self.device_trust_registry[obs.device_id] = round(current_trust, 1)
                source_status = "CONSISTENT"
                valid_weighted_sum += obs.value * (current_trust / 100.0)
                valid_weight += (current_trust / 100.0)

            source_evals.append({
                "device_id": obs.device_id,
                "source": obs.source,
                "reported_value": obs.value,
                "unit": obs.unit,
                "trust_score": round(current_trust, 1),
                "status": source_status,
                "deviation": round(deviation, 2)
            })

        final_trusted_value = (valid_weighted_sum / valid_weight) if valid_weight > 0 else raw_weighted_mean
        status = "TRUSTED"
        if conflicts:
            status = "DATA_INTEGRITY_CONFLICT" if len(conflicts) < len(observations) else "UNTRUSTED"

        return {
            "parameter": parameter_name,
            "trusted_value": round(final_trusted_value, 2),
            "unit": observations[0].unit,
            "confidence": round(min(0.98, max(0.40, (valid_weight / max(1, len(observations))))), 2),
            "status": status,
            "sources": source_evals,
            "warnings": conflicts,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def get_device_trust(self, device_id: str) -> float:
        return self.device_trust_registry.get(device_id, 85.0)

    def reset_device_trust(self, device_id: Optional[str] = None) -> None:
        if device_id and device_id in self.device_trust_registry:
            self.device_trust_registry[device_id] = 94.0
        else:
            for k in self.device_trust_registry:
                self.device_trust_registry[k] = 95.0

trust_engine = TrustEngine()
