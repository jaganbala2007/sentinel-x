"""
Sentinel-X Disaster Intelligence & Scenario Trigger API Router
================================================================
Handles real-time disaster risk scoring, scenario triggers, lifecycle transitions,
and SIH PS 26223 demonstration workflows.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional
import uuid

from app.services.twin_state_manager import twin_state_manager
from app.services.disaster_risk_engine import risk_engine
from app.services.multi_sensor_correlation import correlation_engine
from app.services.disaster_state_machine import disaster_state_machine
from app.services.zone_manager import zone_manager
from app.services.evacuation_manager import evacuation_manager
from app.services.scenario_engine import scenario_engine
from app.services.post_disaster_engine import post_disaster_engine

router = APIRouter(prefix="/api/v1/disasters", tags=["Disaster Intelligence"])

@router.get("/current")
def get_current_disaster_intelligence():
    state = twin_state_manager.get_authoritative_state()
    return {
        "risk_score": state["riskScore"],
        "risk_level": state["riskLevel"],
        "disaster_lifecycle": state["disasterLifecycleState"],
        "safety_decision": state["safetyDecision"],
        "safety_detail": state["safetyDetail"],
        "active_incidents": len(state["incidents"]),
        "zones": state["zones"]
    }

@router.get("/scenarios")
def list_disaster_scenarios():
    return {
        "scenarios": scenario_engine.get_available_scenarios()
    }

@router.post("/scenarios/{scenario_id}/trigger")
def trigger_disaster_scenario(scenario_id: str, payload: Dict[str, Any] = Body(default={})):
    step_idx = int(payload.get("step_index", 2))
    scenario_data = scenario_engine.get_step_telemetry(scenario_id, step_idx)
    
    # Inject simulated telemetry into twin_state_manager
    telem = scenario_data["telemetry"]
    twin_state_manager.update_node1(telem)
    twin_state_manager.update_node2(telem)
    
    # Create matching incident
    inc_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    incident = {
        "id": inc_id,
        "timestamp": twin_state_manager.get_authoritative_state()["node1"].get("lastSeen", ""),
        "node": "NODE-01 / NODE-02",
        "zone": scenario_data["zone_id"],
        "disaster_type": scenario_data["scenario_id"],
        "trigger": scenario_data["scenario_name"],
        "severity": "CRITICAL" if step_idx >= 2 else "WARNING",
        "status": "DETECTED",
        "operator": "JUDGE_DEMO_SIMULATOR",
        "evidence": [scenario_data["description"], "Multi-Sensor Edge Correlation Verification"]
    }
    
    twin_state_manager.incidents.insert(0, incident)
    disaster_state_machine.transition_to("CRITICAL" if step_idx >= 2 else "WARNING", f"Triggered scenario {scenario_id}", "JUDGE_DEMO", inc_id, scenario_data["zone_id"])
    zone_manager.update_zone_status(scenario_data["zone_id"], "CRITICAL" if step_idx >= 2 else "WARNING", 3, "EVACUATE")

    return {
        "status": "SCENARIO_TRIGGERED",
        "scenario": scenario_data,
        "incident": incident,
        "state": twin_state_manager.get_authoritative_state()
    }

@router.post("/reset")
def reset_disaster_system():
    twin_state_manager.recover()
    disaster_state_machine.transition_to("NORMAL", "System administrative reset", "COMMANDER")
    evacuation_manager.reset_evacuation()
    for z in ["ZONE_A", "ZONE_B", "ZONE_C", "ZONE_D"]:
        zone_manager.update_zone_status(z, "NORMAL", 0, "SAFE")
    return {"status": "RESET_COMPLETE", "state": twin_state_manager.get_authoritative_state()}
