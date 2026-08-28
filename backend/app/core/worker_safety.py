"""
Sentinel-X Worker Safety DNA Subsystem
======================================
Maintains real-time Worker Digital DNA profiles, evaluates PPE compliance,
authorizations, environmental exposure, proximity hazards, and computes
the multi-factor dynamic Worker Safety Score (0-100).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class WorkerDNA(BaseModel):
    worker_id: str
    role: str
    department: str
    authorized_zones: List[str]
    authorized_machines: List[str]
    training_certified: bool
    ppe_compliant: bool
    current_zone: str
    current_activity: str
    heart_rate_bpm: int
    fatigue_coefficient: float  # 0.0 alert to 1.0 fatigued
    proximity_machine_id: Optional[str] = None
    proximity_distance_m: Optional[float] = None
    exposure_history: List[str] = Field(default_factory=list)
    near_miss_count: int = 0
    safety_score: float = 100.0
    risk_level: str = "SAFE"
    safety_state: str = "NOMINAL"
    last_seen: datetime = Field(default_factory=datetime.utcnow)


class WorkerSafetyEngine:
    def __init__(self):
        # Demo Worker Digital DNA registry (WRK-001 through WRK-014)
        self.workers: Dict[str, WorkerDNA] = {
            "WRK-001": WorkerDNA(
                worker_id="WRK-001",
                role="Senior Plant Operator",
                department="Operations",
                authorized_zones=["Zone-A", "Zone-B", "Zone-C", "Zone-D"],
                authorized_machines=["M-001", "M-002", "M-007"],
                training_certified=True,
                ppe_compliant=True,
                current_zone="Zone-A",
                current_activity="Routine Control Loop Inspection",
                heart_rate_bpm=74,
                fatigue_coefficient=0.15,
                proximity_machine_id="M-001",
                proximity_distance_m=4.2,
                safety_score=96.0,
                risk_level="SAFE"
            ),
            "WRK-007": WorkerDNA(
                worker_id="WRK-007",
                role="Mechanical Maintenance Tech",
                department="Maintenance",
                authorized_zones=["Zone-A", "Zone-B", "Zone-C"],
                authorized_machines=["M-001", "M-003", "M-007"],
                training_certified=True,
                ppe_compliant=True,
                current_zone="Zone-B",
                current_activity="Bearing Vibration Diagnostics",
                heart_rate_bpm=82,
                fatigue_coefficient=0.28,
                proximity_machine_id="M-007",
                proximity_distance_m=2.1,
                safety_score=88.0,
                risk_level="LOW"
            ),
            "WRK-014": WorkerDNA(
                worker_id="WRK-014",
                role="Junior Field Specialist",
                department="Logistics & Assembly",
                authorized_zones=["Zone-A", "Zone-C"],
                authorized_machines=["M-002", "M-004"],
                training_certified=True,
                ppe_compliant=True,
                current_zone="Zone-B",  # Intrusion into unauthorized Zone-B
                current_activity="Material Transit",
                heart_rate_bpm=108,
                fatigue_coefficient=0.62,
                proximity_machine_id="M-007",
                proximity_distance_m=1.1,  # Dangerous proximity to M-007
                exposure_history=["Elevated Thermal Zone", "Restricted Area Intrusion"],
                near_miss_count=1,
                safety_score=58.0,
                risk_level="HIGH",
                safety_state="ZONE_UNAUTHORIZED_AND_HAZARD_PROXIMITY"
            ),
        }

    def compute_worker_safety_score(
        self,
        worker_id: str,
        machine_risk_scores: Optional[Dict[str, float]] = None,
        env_risk_scores: Optional[Dict[str, float]] = None
    ) -> WorkerDNA:
        """
        Calculates dynamic multi-factor safety score (0-100) for a given worker.
        Deductions:
          - PPE non-compliance: -35 pts
          - Unauthorized zone: -30 pts
          - High fatigue (>0.6): -15 pts
          - Hazardous machine proximity (< 2.0m to machine with high risk): -25 pts
          - Elevated environmental zone risk: -15 pts
        """
        if worker_id not in self.workers:
            raise KeyError(f"Worker {worker_id} not found in Digital DNA registry.")

        w = self.workers[worker_id]
        score = 100.0
        factors = []

        # 1. PPE Compliance
        if not w.ppe_compliant:
            score -= 35.0
            factors.append("PPE Violation (-35)")

        # 2. Zone Authorization
        if w.current_zone not in w.authorized_zones:
            score -= 30.0
            factors.append(f"Unauthorized Zone {w.current_zone} Access (-30)")

        # 3. Fatigue Coefficient
        if w.fatigue_coefficient > 0.6:
            score -= 15.0
            factors.append(f"Critical Fatigue Level {w.fatigue_coefficient*100:.0f}% (-15)")
        elif w.fatigue_coefficient > 0.4:
            score -= 8.0
            factors.append(f"Moderate Fatigue {w.fatigue_coefficient*100:.0f}% (-8)")

        # 4. Proximity to hazardous machinery
        if w.proximity_machine_id and w.proximity_distance_m is not None:
            m_risk = (machine_risk_scores or {}).get(w.proximity_machine_id, 20.0)
            if w.proximity_distance_m < 1.5 and m_risk > 70.0:
                score -= 30.0
                factors.append(f"Severe Proximity ({w.proximity_distance_m}m) to High-Risk Machine {w.proximity_machine_id} (-30)")
            elif w.proximity_distance_m < 2.5 and m_risk > 50.0:
                score -= 15.0
                factors.append(f"Close Proximity ({w.proximity_distance_m}m) to Degraded Machine {w.proximity_machine_id} (-15)")

        # 5. Environmental zone risk
        zone_env_risk = (env_risk_scores or {}).get(w.current_zone, 10.0)
        if zone_env_risk > 60.0:
            score -= 20.0
            factors.append(f"Harsh Environment in {w.current_zone} (-20)")

        final_score = max(0.0, min(100.0, score))
        w.safety_score = round(final_score, 1)

        if final_score >= 85.0:
            w.risk_level = "SAFE"
            w.safety_state = "NOMINAL"
        elif final_score >= 70.0:
            w.risk_level = "LOW"
            w.safety_state = "ATTENTION_REQUIRED"
        elif final_score >= 50.0:
            w.risk_level = "MEDIUM"
            w.safety_state = "ELEVATED_RISK"
        elif final_score >= 30.0:
            w.risk_level = "HIGH"
            w.safety_state = "CRITICAL_HAZARD"
        else:
            w.risk_level = "CRITICAL"
            w.safety_state = "EMERGENCY_INTERVENTION_REQUIRED"

        w.last_seen = datetime.utcnow()
        return w

    def list_all_workers(self) -> List[Dict[str, Any]]:
        return [w.model_dump() for w in self.workers.values()]

    def get_worker(self, worker_id: str) -> Optional[Dict[str, Any]]:
        if worker_id in self.workers:
            return self.workers[worker_id].model_dump()
        return None

    def update_worker_location(self, worker_id: str, zone: str, machine_id: Optional[str] = None, dist_m: Optional[float] = None) -> WorkerDNA:
        if worker_id not in self.workers:
            raise KeyError(f"Worker {worker_id} not registered.")
        w = self.workers[worker_id]
        w.current_zone = zone
        w.proximity_machine_id = machine_id
        w.proximity_distance_m = dist_m
        return self.compute_worker_safety_score(worker_id)


worker_safety_engine = WorkerSafetyEngine()
