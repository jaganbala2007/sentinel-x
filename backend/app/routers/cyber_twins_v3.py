"""
Sentinel-X Cyber-Resilient Digital Twin API Router (v3.0)
=========================================================
Exposes unified endpoints for Worker Safety DNA, Machine Safety DNA,
Sensor Trust, Cyber/Data Integrity Simulation, Machine Health & RUL,
What-If Simulations, Incident Reconstruction, and AI Copilot.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.worker_safety import worker_safety_engine
from app.core.machine_safety import machine_safety_engine
from app.core.trust_engine import trust_engine, SensorObservation
from app.core.cyber_integrity_engine import cyber_integrity_engine
from app.core.rul_engine import rul_engine
from app.core.environment_safety import environment_safety_engine
from app.core.risk_engine import unified_risk_engine
from app.core.what_if_engine import what_if_engine, WhatIfRequest
from app.core.decision_engine import safety_decision_engine
from app.core.incident_engine import incident_reconstruction_engine
from app.core.copilot_engine import industrial_ai_copilot

router = APIRouter()


# ---------------------------------------------------------------------------
# 1. Worker Digital DNA Endpoints
# ---------------------------------------------------------------------------

@router.get("/workers", summary="List all Worker Digital DNA profiles")
async def get_all_workers() -> List[Dict[str, Any]]:
    return worker_safety_engine.list_all_workers()


@router.get("/workers/{worker_id}", summary="Get specific Worker Safety DNA profile")
async def get_worker_profile(worker_id: str) -> Dict[str, Any]:
    w = worker_safety_engine.get_worker(worker_id)
    if not w:
        raise HTTPException(status_code=404, detail=f"Worker '{worker_id}' not found.")
    return w


# ---------------------------------------------------------------------------
# 2. Machine Safety DNA & RUL Endpoints
# ---------------------------------------------------------------------------

@router.get("/machines", summary="List all Machine Safety DNA profiles")
async def get_all_machines() -> List[Dict[str, Any]]:
    return machine_safety_engine.list_all_machines()


@router.get("/machines/{machine_id}", summary="Get Machine Safety DNA profile")
async def get_machine_profile(machine_id: str) -> Dict[str, Any]:
    m = machine_safety_engine.get_machine(machine_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Machine '{machine_id}' not found.")
    return m


@router.get("/machines/{machine_id}/health", summary="Compute real-time Health Index and RUL")
async def get_machine_health_and_rul(
    machine_id: str,
    temp_c: float = Query(72.0, description="Current temperature in Celsius"),
    vibration_mm_s: float = Query(3.5, description="Vibration in mm/s"),
    current_a: float = Query(35.0, description="Current in Amperes"),
    rpm: float = Query(3000.0, description="Rotational speed in RPM")
) -> Dict[str, Any]:
    return rul_engine.compute_health_and_rul(machine_id, temp_c, vibration_mm_s, current_a, rpm)


# ---------------------------------------------------------------------------
# 3. Sensor Trust & Cyber-Integrity Endpoints
# ---------------------------------------------------------------------------

@router.get("/trust/status", summary="Get device trust score registry")
async def get_trust_registry() -> Dict[str, Any]:
    return {
        "version": "3.0.0",
        "device_trust_scores": trust_engine.device_trust_registry,
        "active_simulation": cyber_integrity_engine.active_scenario_name
    }


class SensorValidationRequest(BaseModel):
    parameter_name: str
    observations: List[Dict[str, Any]]


@router.post("/trust/validate", summary="Run multi-sensor consensus and consistency validation")
async def validate_sensors(req: SensorValidationRequest) -> Dict[str, Any]:
    obs_list = [
        SensorObservation(
            parameter=o.get("parameter", req.parameter_name),
            value=float(o["value"]),
            unit=o.get("unit", ""),
            source=o.get("source", "SENSOR"),
            device_id=o["device_id"]
        )
        for o in req.observations
    ]
    return trust_engine.evaluate_sensor_consensus(req.parameter_name, obs_list)


@router.post("/cyber/simulate-hero", summary="Execute Hero Scenario 1 (82°C physical vs 42°C manipulated PLC)")
async def simulate_hero_attack() -> Dict[str, Any]:
    return cyber_integrity_engine.run_hero_scenario_1(simulate_manipulation=True)


@router.post("/cyber/reset", summary="Reset cyber attack simulation to nominal state")
async def reset_cyber_simulation() -> Dict[str, Any]:
    return cyber_integrity_engine.reset_simulation()


# ---------------------------------------------------------------------------
# 4. Unified Risk & Environment Safety
# ---------------------------------------------------------------------------

@router.get("/safety/risk", summary="Compute plant-wide and asset-level unified risk")
async def get_unified_plant_risk() -> Dict[str, Any]:
    return unified_risk_engine.evaluate_global_plant_risk()


@router.get("/safety/environment", summary="Get multi-zone environmental telemetry")
async def get_environment_zones() -> List[Dict[str, Any]]:
    return environment_safety_engine.list_zones()


@router.post("/safety/decisions/evaluate", summary="Run safety decision engine")
async def evaluate_safety_decision() -> Dict[str, Any]:
    d = safety_decision_engine.evaluate_and_decide()
    return d.model_dump()


# ---------------------------------------------------------------------------
# 5. What-If Digital Twin Simulation
# ---------------------------------------------------------------------------

@router.post("/simulations/what-if", summary="Run hypothetical operational stress simulation")
async def run_what_if_simulation(req: WhatIfRequest) -> Dict[str, Any]:
    return what_if_engine.simulate_scenario(req)


# ---------------------------------------------------------------------------
# 6. Incident Reconstruction Timeline
# ---------------------------------------------------------------------------

@router.get("/incidents/hero-timeline", summary="Get Hero Incident timeline reconstruction")
async def get_hero_incident_timeline() -> Dict[str, Any]:
    return incident_reconstruction_engine.get_hero_incident_reconstruction()


# ---------------------------------------------------------------------------
# 7. Industrial AI Copilot
# ---------------------------------------------------------------------------

class CopilotQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question for the AI Copilot")


@router.post("/copilot/query", summary="Query the Sentinel-X AI Copilot")
async def query_copilot(req: CopilotQueryRequest) -> Dict[str, Any]:
    return industrial_ai_copilot.answer_query(req.query)
