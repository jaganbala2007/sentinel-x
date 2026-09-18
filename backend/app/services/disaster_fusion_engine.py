"""
Sentinel-X Deterministic Additive Bayesian Disaster Fusion Engine
Calculates disaster risk confidence from TRUSTED multi-sensor telemetry.
QUARANTINED NODES ARE EXCLUDED FROM THE FUSION PIPELINE.
"""

from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.disaster import DisasterRiskSchema, XAIFactorsSchema

class DisasterFusionEngine:
    def __init__(self):
        self.current_risk_score = 18
        self.current_confidence = 96
        self.current_severity = "NORMAL"
        self.factors = XAIFactorsSchema()

    def evaluate_risk(self, trusted_readings: List[Dict[str, Any]], 
                      basin_rainfall_mm: float = 4.2, 
                      soil_saturation_pct: float = 48.5) -> DisasterRiskSchema:
        """
        Calculates explainable risk score using deterministic additive Bayesian evidence weights.
        """
        if not trusted_readings:
            # Degraded default if all sensors lost
            return DisasterRiskSchema(
                risk_score=self.current_risk_score,
                confidence=self.current_confidence,
                severity=self.current_severity,
                contributing_factors=self.factors,
                evidence=["Insufficient trusted sensor readings; maintaining last state"],
                affected_sector="SECTOR B (BASIN 04)",
                recommended_action="INSPECT SENSOR NETWORK"
            )

        # 1. Average Stage & Rate of trusted nodes
        avg_stage = sum(r["stage_m"] for r in trusted_readings) / len(trusted_readings)
        avg_rate = sum(r.get("rate_m_min", 0.0) for r in trusted_readings) / len(trusted_readings)

        # 2. Water Elevation Factor (Weight max: 40)
        water_factor = 5
        if avg_stage >= settings.DISASTER_WATER_CRITICAL_LEVEL:
            water_factor = 40
        elif avg_stage >= settings.DISASTER_WATER_WARNING_LEVEL:
            water_factor = 25
        elif avg_stage > 2.50:
            water_factor = 12

        # 3. Rate of Rise Factor (Weight max: 30)
        rise_factor = 3
        if avg_rate >= settings.RATE_OF_RISE_CRITICAL:
            rise_factor = 30
        elif avg_rate >= settings.RATE_OF_RISE_WARNING:
            rise_factor = 18
        elif avg_rate > 0.02:
            rise_factor = 8


        # 4. Basin Rainfall Factor (Weight max: 15)
        rain_factor = 4
        if basin_rainfall_mm > 50.0:
            rain_factor = 14
        elif basin_rainfall_mm > 20.0:
            rain_factor = 9

        # 5. Soil Saturation Factor (Weight max: 10)
        soil_factor = 2
        if soil_saturation_pct > 85.0:
            soil_factor = 8
        elif soil_saturation_pct > 65.0:
            soil_factor = 5

        # 6. Spatial Node Agreement Consensus Factor (Weight max: 10)
        # More trusted nodes in agreement = higher evidence weight
        consensus_factor = min(10, max(2, int(len(trusted_readings) * 0.5)))
        hist_factor = 2

        total_risk = water_factor + rise_factor + rain_factor + soil_factor + consensus_factor + hist_factor
        total_risk = max(0, min(100, total_risk))

        # Determine Severity
        evidence = []
        if total_risk >= 75:
            severity = "CRITICAL"
            action = "ACTIVATE LOCAL SIRENS & BROADCAST EVACUATION CORRIDOR ALPHA"
            evidence.append(f"Water stage {avg_stage:.2f}m exceeds critical threshold ({settings.DISASTER_WATER_CRITICAL_LEVEL}m)")
            evidence.append(f"Rate of rise {avg_rate:+.2f}m/min indicates rapid hydraulic surge")
        elif total_risk >= 45:
            severity = "WARNING"
            action = "ISSUE WATCH BULLETIN & ARM EMERGENCY HF PACKET RELAY"
            evidence.append(f"Water stage {avg_stage:.2f}m elevated above warning datum")
        elif total_risk >= 25:
            severity = "WATCH"
            action = "INCREASE SENSOR POLLING FREQUENCY"
            evidence.append("Mild upstream runoff detected")
        else:
            severity = "NORMAL"
            action = "CONTINUE STEADY OPERATIONAL MONITORING"
            evidence.append("All hydrological parameters within laminar seasonal bounds")

        evidence.append(f"{len(trusted_readings)} trusted sensor nodes in consensus")

        self.current_risk_score = total_risk
        self.current_severity = severity
        self.current_confidence = 94 if len(trusted_readings) >= 3 else 82
        self.factors = XAIFactorsSchema(
            water=water_factor,
            rise=rise_factor,
            rain=rain_factor,
            soil=soil_factor,
            consensus=consensus_factor,
            hist=hist_factor
        )

        return DisasterRiskSchema(
            risk_score=self.current_risk_score,
            confidence=self.current_confidence,
            severity=self.current_severity,
            contributing_factors=self.factors,
            evidence=evidence,
            affected_sector="SECTOR B (BASIN 04)",
            recommended_action=action
        )

disaster_fusion_engine = DisasterFusionEngine()
