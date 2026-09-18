"""
Sentinel-X V2 Universal Risk Engine
===================================
Environment-agnostic Multi-Hazard Risk Intelligence & Decision Engine.
Coordinates:
  1. Byzantine sensor trust verification via UniversalSensorTrustEngine
  2. Pluggable hazard assessment across active EnvironmentProfile hazards
  3. Multi-hazard compounding risk synthesis and policy response generation
"""

from typing import List, Dict, Optional, Any
from app.schemas.universal import (
    NormalizedSensorReading,
    EnvironmentProfile,
    MultiHazardRiskAssessment,
    HazardAssessment,
    HazardType,
    SeverityLevel
)
from app.services.universal_trust_engine import universal_trust_engine
from app.services.hazard_engine import hazard_registry
from app.services.environment_manager import environment_manager

class UniversalRiskEngine:
    def evaluate_environment(
        self,
        readings: Optional[List[NormalizedSensorReading]] = None,
        profile: Optional[EnvironmentProfile] = None
    ) -> MultiHazardRiskAssessment:
        if profile is None:
            profile = environment_manager.get_active_profile()
            
        if readings is None or len(readings) == 0:
            readings = environment_manager.generate_baseline_readings()

        # Step 1: Evaluate Sensor Trust for all incoming readings
        trust_results = universal_trust_engine.evaluate_batch(readings, profile)
        trust_map = {node_id: res["trust_score"] for node_id, res in trust_results.items()}
        quarantined_nodes = [
            node_id for node_id, res in trust_results.items() 
            if res["status"] == "QUARANTINED"
        ]

        # Step 2: Evaluate Active Hazards using Pluggable Hazard Engine
        hazard_assessments = hazard_registry.evaluate_active_hazards(readings, trust_map, profile)

        # Fallback if no hazards triggered
        if not hazard_assessments:
            return MultiHazardRiskAssessment(
                environment=profile.id,
                overall_risk_score=10,
                overall_confidence=95,
                overall_severity=SeverityLevel.NORMAL,
                primary_threat=HazardType.FLASH_FLOOD,
                active_hazard_assessments=[],
                contributing_factors={"baseline": 10},
                evidence_chain=["All monitored metrics operating within normal baseline limits"],
                affected_sector="ALL SECTORS SECURE",
                recommended_operational_action="MAINTAIN NORMAL MONITORING SCHEDULE"
            )

        # Step 3: Multi-Hazard Compounding & Highest Threat Synthesis
        # Sort hazards by risk score descending
        sorted_hazards = sorted(hazard_assessments, key=lambda h: h.risk_score, reverse=True)
        primary_hazard = sorted_hazards[0]
        
        # Base risk from primary hazard
        overall_risk = primary_hazard.risk_score
        
        # If secondary hazards are also elevated, apply compounding factor
        secondary_risks = [h.risk_score for h in sorted_hazards[1:] if h.risk_score >= 40]
        if secondary_risks:
            compounding_bonus = min(15, len(secondary_risks) * 8)
            overall_risk = min(100, overall_risk + compounding_bonus)

        # Overall Confidence
        avg_confidence = int(sum(h.confidence for h in hazard_assessments) / len(hazard_assessments))

        # Overall Severity
        if overall_risk >= 75:
            overall_sev = SeverityLevel.CRITICAL
        elif overall_risk >= 50:
            overall_sev = SeverityLevel.WARNING
        elif overall_risk >= 25:
            overall_sev = SeverityLevel.WATCH
        else:
            overall_sev = SeverityLevel.NORMAL

        # Evidence Chain aggregation
        evidence_chain = []
        for h in hazard_assessments:
            evidence_chain.extend(h.evidence)

        if quarantined_nodes:
            evidence_chain.append(f"Byzantine Quarantine Active: Isolated {len(quarantined_nodes)} anomalous node(s) ({', '.join(quarantined_nodes)})")

        contributing_factors = {
            h.hazard_type.value: h.risk_score for h in hazard_assessments
        }

        return MultiHazardRiskAssessment(
            environment=profile.id,
            overall_risk_score=overall_risk,
            overall_confidence=avg_confidence,
            overall_severity=overall_sev,
            primary_threat=primary_hazard.hazard_type,
            active_hazard_assessments=hazard_assessments,
            contributing_factors=contributing_factors,
            evidence_chain=evidence_chain,
            affected_sector=primary_hazard.affected_zone,
            recommended_operational_action=primary_hazard.recommended_action
        )

universal_risk_engine = UniversalRiskEngine()
