"""
Sentinel-X V2 Universal Sensor Trust Engine
===========================================
Environment-agnostic Byzantine sensor verification engine.
Dynamically validates physical plausibility, rate-of-change invariants,
cross-sensor correlations, and multi-node spatial consensus based on the
active sensor definitions.
"""

from typing import List, Dict, Optional, Any
from app.schemas.universal import (
    NormalizedSensorReading,
    SensorDefinition,
    TrustStatus,
    EnvironmentProfile
)

class UniversalSensorTrustEngine:
    def __init__(self):
        # Historical buffer: hist_key -> list of readings
        self.history: Dict[str, List[NormalizedSensorReading]] = {}

    def reset(self):
        """Clear all historical state between test runs or simulation resets."""
        self.history.clear()

    def evaluate_node(
        self,
        reading: NormalizedSensorReading,
        sensor_def: Optional[SensorDefinition],
        all_current_readings: List[NormalizedSensorReading]
    ) -> Dict[str, Any]:
        """
        Evaluate a single reading against physical invariants, historical rate of change,
        and Byzantine spatial neighbor consensus.
        """
        reasons = []
        score = 100.0

        # Fallback bounds if sensor definition not provided
        min_bound = sensor_def.min_plausible if sensor_def else -50.0
        max_bound = sensor_def.max_plausible if sensor_def else 10000.0
        max_rate = sensor_def.max_rate_of_change if sensor_def else 50.0

        # 1. Physical Plausibility Range Invariant
        if reading.value < min_bound or reading.value > max_bound:
            score -= 60.0
            reasons.append(
                f"Reading {reading.value} {reading.unit} violates physical bounds "
                f"[{min_bound}, {max_bound}] {reading.unit}"
            )

        # 2. Kinematic Rate-of-Change Invariant (keyed by node_id and metric_name)
        hist_key = f"{reading.node_id}:{reading.metric_name}"
        node_hist = self.history.get(hist_key, [])
        if node_hist:
            prev = node_hist[-1]
            dt_min = max(0.01, (reading.timestamp_ms - prev.timestamp_ms) / 60000.0)
            rate = abs(reading.value - prev.value) / dt_min
            if rate > max_rate:
                score -= 40.0
                reasons.append(
                    f"Implausible rate of change: {rate:.2f} {reading.unit}/min "
                    f"(limit: {max_rate:.2f})"
                )

        # 3. Byzantine Spatial Neighbor Consensus
        # Find other current readings measuring the exact same metric
        peers = [
            r for r in all_current_readings 
            if r.metric_name == reading.metric_name and r.node_id != reading.node_id
        ]
        if len(peers) >= 2:
            peer_values = [r.value for r in peers]
            median_val = float(np.median(peer_values))
            std_dev = float(np.std(peer_values)) or 0.1
            tolerance = max(std_dev * 3.0, (max_bound - min_bound) * 0.10)
            
            diff = abs(reading.value - median_val)
            if diff > tolerance * 2.0:
                score -= 85.0
                reasons.append(
                    f"Extreme Byzantine disagreement: reported {reading.value} {reading.unit}, "
                    f"peer consensus median is {median_val:.2f} {reading.unit} (diff {diff:.2f} >> tol {tolerance:.2f})"
                )
            elif diff > tolerance:
                score -= 50.0
                reasons.append(
                    f"Byzantine disagreement: reported {reading.value} {reading.unit}, "
                    f"peer consensus median is {median_val:.2f} {reading.unit} (diff {diff:.2f} > tol {tolerance:.2f})"
                )

        # 4. Hardware Health & Battery Degradation
        if reading.hardware_health != "HEALTHY":
            score -= 20.0
            reasons.append(f"Hardware health flag: {reading.hardware_health}")

        if reading.battery_pct < 15:
            score -= 15.0
            reasons.append(f"Critical battery depletion ({reading.battery_pct}%) inducing ADC drift")

        # Clamp score
        final_score = max(0.0, min(100.0, score))

        # Categorize Trust Status
        if final_score >= 85.0:
            status = TrustStatus.VERIFIED
        elif final_score >= 65.0:
            status = TrustStatus.TRUSTED
        elif final_score >= 40.0:
            status = TrustStatus.SUSPICIOUS
        elif final_score >= 20.0:
            status = TrustStatus.DEGRADED
        else:
            status = TrustStatus.QUARANTINED

        # Append to history (bounded window of 20 samples per metric)
        if hist_key not in self.history:
            self.history[hist_key] = []
        self.history[hist_key].append(reading)
        if len(self.history[hist_key]) > 20:
            self.history[hist_key].pop(0)

        return {
            "node_id": reading.node_id,
            "metric_name": reading.metric_name,
            "trust_score": round(final_score, 1),
            "status": status.value,
            "reasons": reasons if reasons else ["Conforms to physical bounds, rate limits, and neighbor consensus"],
            "raw_value": reading.value,
            "unit": reading.unit
        }

    def evaluate_batch(
        self,
        readings: List[NormalizedSensorReading],
        profile: EnvironmentProfile
    ) -> Dict[str, Dict[str, Any]]:
        # Map sensor definitions by metric_name
        defs_by_metric = {d.metric_name: d for d in profile.sensor_definitions}
        
        trust_results = {}
        for r in readings:
            s_def = defs_by_metric.get(r.metric_name)
            res = self.evaluate_node(r, s_def, readings)
            trust_results[r.node_id] = res
            
        return trust_results

universal_trust_engine = UniversalSensorTrustEngine()
