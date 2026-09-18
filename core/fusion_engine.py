"""
Sentinel-X Core: Multi-Sensor Evidence Fusion Engine
=====================================================
Combines redundant and heterogeneous sensor observations into a verified evidence vector.
Weights readings by individual Sensor Trust Scores.
Discards quarantined sensors to prevent Byzantine spoofing or false alarm propagation.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from core.sensor_abstraction import SensorReading, SensorTrustStatus

class FusedParameter(BaseModel):
    parameter: str
    fused_value: float
    unit: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    contributing_sensors: List[str]
    quarantined_sensors: List[str]
    dispersion_variance: float = 0.0

class MultiSensorFusionEngine:
    def __init__(self):
        pass

    def fuse_readings(self, parameter: str, readings: List[SensorReading]) -> FusedParameter:
        """
        Bayesian & trust-weighted sensor consensus fusion.
        Excludes QUARANTINED sensors.
        Weights each reading by (trust_score / 100.0) * voting_weight.
        """
        if not readings:
            return FusedParameter(
                parameter=parameter, fused_value=0.0, unit="",
                confidence=0.0, contributing_sensors=[], quarantined_sensors=[]
            )

        valid_readings = []
        quarantined = []

        for r in readings:
            if r.trust_status == SensorTrustStatus.QUARANTINED or r.voting_weight <= 0.0:
                quarantined.append(r.sensor_id)
            else:
                valid_readings.append(r)

        if not valid_readings:
            # Fallback if all sensors quarantined
            primary = readings[0]
            return FusedParameter(
                parameter=parameter, fused_value=primary.value, unit=primary.unit,
                confidence=0.1, contributing_sensors=[], quarantined_sensors=quarantined
            )

        total_weight = 0.0
        weighted_sum = 0.0
        contributing = []

        for r in valid_readings:
            effective_weight = max(0.05, (r.trust_score / 100.0) * r.voting_weight)
            weighted_sum += r.value * effective_weight
            total_weight += effective_weight
            contributing.append(r.sensor_id)

        fused_val = weighted_sum / total_weight if total_weight > 0 else valid_readings[0].value

        # Calculate dispersion / variance
        if len(valid_readings) > 1:
            variance = sum((r.value - fused_val) ** 2 for r in valid_readings) / len(valid_readings)
        else:
            variance = 0.0

        # Confidence is average trust of contributing sensors normalized
        avg_trust = sum(r.trust_score for r in valid_readings) / (100.0 * len(valid_readings))
        confidence = round(avg_trust * (1.0 / (1.0 + (variance * 0.05))), 3)

        return FusedParameter(
            parameter=parameter,
            fused_value=round(fused_val, 2),
            unit=valid_readings[0].unit,
            confidence=min(1.0, max(0.05, confidence)),
            contributing_sensors=contributing,
            quarantined_sensors=quarantined,
            dispersion_variance=round(variance, 4)
        )

fusion_engine = MultiSensorFusionEngine()
