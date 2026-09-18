"""
Sentinel-X Hazards: Human Worker Safety & Machine Zone Conflict
================================================================
Evaluates:
  - Optical / ToF LiDAR worker proximity to hazardous conveyor pinch-points
  - Emergency pull-wire interlock circuit state
  - Worker-machine operational conflict (conveyor moving while operator inside perimeter)
"""

from pydantic import BaseModel

class WorkerHazardAssessment(BaseModel):
    hazard_name: str = "Worker Zone Safety & Interlocks"
    severity_level: str = "NORMAL"
    risk_score: float = 0.0
    worker_proximity_m: float = 4.5
    estop_tripped: bool = False
    conflict_detected: bool = False
    diagnosis: str = "Restricted pinch-point perimeter clear. E-Stop closed."
    recommended_action: str = "Standard safety interlocks armed."

class WorkerSafetyHazardModule:
    def evaluate(self, worker_proximity_m: float, belt_speed: float, estop_tripped: bool = False) -> WorkerHazardAssessment:
        if estop_tripped:
            return WorkerHazardAssessment(
                severity_level="CRITICAL",
                risk_score=98.0,
                worker_proximity_m=worker_proximity_m,
                estop_tripped=True,
                conflict_detected=True,
                diagnosis="CRITICAL: Emergency Stop pull-wire tripped! Safety circuit open.",
                recommended_action="Immediate complete plant cut-off. Sound evacuation beacon."
            )

        # Worker-machine conflict
        if belt_speed > 0.1 and worker_proximity_m < 0.9:
            return WorkerHazardAssessment(
                severity_level="CRITICAL",
                risk_score=95.0,
                worker_proximity_m=worker_proximity_m,
                estop_tripped=False,
                conflict_detected=True,
                diagnosis="CRITICAL SAFETY VIOLATION: Worker inside rotating pinch-point zone while conveyor active!",
                recommended_action="Trigger autonomous hardware e-stop trip immediately, flash red strobe, and blast 110dB siren."
            )
        elif worker_proximity_m < 1.8:
            return WorkerHazardAssessment(
                severity_level="WARNING",
                risk_score=60.0,
                worker_proximity_m=worker_proximity_m,
                estop_tripped=False,
                conflict_detected=False,
                diagnosis="WARNING: Personnel approaching restricted conveyor boundary.",
                recommended_action="Flash yellow warning beacon and chime operator station buzzer."
            )
        elif worker_proximity_m < 2.5:
            return WorkerHazardAssessment(
                severity_level="WATCH",
                risk_score=28.0,
                worker_proximity_m=worker_proximity_m,
                estop_tripped=False,
                conflict_detected=False,
                diagnosis="WATCH: Worker detected in outer walkway buffer.",
                recommended_action="Display optical indicator on local SCADA mimic."
            )

        return WorkerHazardAssessment(
            severity_level="NORMAL",
            risk_score=5.0,
            worker_proximity_m=worker_proximity_m,
            estop_tripped=False,
            conflict_detected=False,
            diagnosis="Restricted pinch-point perimeter clear. E-Stop closed.",
            recommended_action="Standard safety interlocks armed."
        )

worker_safety_hazard_module = WorkerSafetyHazardModule()
