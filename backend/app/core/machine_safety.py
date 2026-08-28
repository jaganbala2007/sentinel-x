"""
Sentinel-X Machine Safety DNA Subsystem
=======================================
Maintains deep engineering profiles for plant machinery (M-001 to M-010),
including operational envelopes, wear histories, and critical components.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MachineDNA(BaseModel):
    machine_id: str
    name: str
    machine_type: str
    zone: str
    operating_hours: float
    rated_rpm: float
    max_allowable_temp_c: float
    max_allowable_vibration_mm_s: float
    max_allowable_current_a: float
    critical_components: List[str]
    last_maintenance_date: str
    next_scheduled_maintenance: str
    maintenance_overdue: bool = False
    failure_history: List[Dict[str, Any]] = Field(default_factory=list)


class MachineSafetyEngine:
    def __init__(self):
        self.machines: Dict[str, MachineDNA] = {
            "M-001": MachineDNA(
                machine_id="M-001",
                name="Centrifugal Feed Pump Alpha",
                machine_type="Centrifugal Pump",
                zone="Zone-A",
                operating_hours=4120.5,
                rated_rpm=1780.0,
                max_allowable_temp_c=80.0,
                max_allowable_vibration_mm_s=4.5,
                max_allowable_current_a=32.0,
                critical_components=["Mechanical Seal", "Impeller Shaft", "Thrust Bearing"],
                last_maintenance_date="2026-06-15",
                next_scheduled_maintenance="2026-09-15",
                maintenance_overdue=False
            ),
            "M-002": MachineDNA(
                machine_id="M-002",
                name="Primary Air Compressor 02",
                machine_type="Screw Compressor",
                zone="Zone-A",
                operating_hours=6890.0,
                rated_rpm=2980.0,
                max_allowable_temp_c=85.0,
                max_allowable_vibration_mm_s=5.0,
                max_allowable_current_a=55.0,
                critical_components=["Screw Rotors", "Oil Separator", "Main Drive Bearing"],
                last_maintenance_date="2026-05-10",
                next_scheduled_maintenance="2026-08-10",
                maintenance_overdue=True
            ),
            "M-007": MachineDNA(
                machine_id="M-007",
                name="High-Pressure Rotary Compressor",
                machine_type="Multi-Stage Rotary Compressor",
                zone="Zone-B",
                operating_hours=12480.0,
                rated_rpm=3000.0,
                max_allowable_temp_c=78.0,
                max_allowable_vibration_mm_s=5.5,
                max_allowable_current_a=50.0,
                critical_components=["Bearing Assembly (High Wear)", "Suction Valve Array", "Shaft Coupling"],
                last_maintenance_date="2026-03-01",
                next_scheduled_maintenance="2026-07-01",
                maintenance_overdue=True,
                failure_history=[
                    {"date": "2025-11-14", "component": "Bearing Assembly", "root_cause": "Lubrication Breakdown"},
                    {"date": "2026-02-18", "component": "Shaft Coupling", "root_cause": "Axial Misalignment"}
                ]
            ),
            "M-004": MachineDNA(
                machine_id="M-004",
                name="Continuous Logistics Conveyor Line",
                machine_type="Belt Conveyor",
                zone="Zone-C",
                operating_hours=3200.0,
                rated_rpm=450.0,
                max_allowable_temp_c=65.0,
                max_allowable_vibration_mm_s=3.8,
                max_allowable_current_a=24.0,
                critical_components=["Drive Drum", "Belt Tensioner", "Gearbox"],
                last_maintenance_date="2026-07-01",
                next_scheduled_maintenance="2026-10-01",
                maintenance_overdue=False
            ),
        }

    def get_machine(self, machine_id: str) -> Optional[Dict[str, Any]]:
        if machine_id in self.machines:
            return self.machines[machine_id].model_dump()
        return None

    def list_all_machines(self) -> List[Dict[str, Any]]:
        return [m.model_dump() for m in self.machines.values()]


machine_safety_engine = MachineSafetyEngine()
