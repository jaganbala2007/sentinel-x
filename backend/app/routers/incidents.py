"""
Sentinel-X Disaster Incident Command REST API Router
=====================================================
Handles full disaster incident lifecycle management, commander acknowledgement,
resource assignment, evacuation mode, and post-disaster recovery report retrieval.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

from app.services.twin_state_manager import twin_state_manager
from app.services.disaster_state_machine import disaster_state_machine
from app.services.zone_manager import zone_manager
from app.services.evacuation_manager import evacuation_manager
from app.services.post_disaster_engine import post_disaster_engine
from core.database import get_db_connection

router = APIRouter(prefix="/api/v1/incidents", tags=["Disaster Incidents"])

@router.get("")
def list_incidents():
    return {
        "total": len(twin_state_manager.incidents),
        "incidents": twin_state_manager.incidents
    }

@router.post("")
def create_incident(payload: Dict[str, Any] = Body(...)):
    inc_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    ts = datetime.now(timezone.utc).isoformat()
    
    incident = {
        "id": inc_id,
        "timestamp": ts,
        "zone": payload.get("zone", "ZONE_B"),
        "disaster_type": payload.get("disaster_type", "HAZARD_EVENT"),
        "severity": payload.get("severity", "CRITICAL"),
        "status": "DETECTED",
        "evidence": payload.get("evidence", ["Manual Operator Trigger"]),
        "operator": payload.get("operator", "COMMANDER"),
        "assigned_team": None
    }
    
    twin_state_manager.incidents.insert(0, incident)
    disaster_state_machine.transition_to("INCIDENT", f"Incident {inc_id} created in {incident['zone']}", incident['operator'], inc_id, incident['zone'])
    zone_manager.update_zone_status(incident['zone'], incident['severity'], 3, "EVACUATE")
    
    return incident

@router.post("/{incident_id}/acknowledge")
def acknowledge_incident(incident_id: str, payload: Dict[str, Any] = Body(default={})):
    operator = payload.get("operator", "DISASTER_COMMANDER")
    for inc in twin_state_manager.incidents:
        if inc["id"] == incident_id:
            inc["status"] = "ACKNOWLEDGED"
            inc["acknowledged_at"] = datetime.now(timezone.utc).isoformat()
            disaster_state_machine.transition_to("RESPONSE", f"Incident {incident_id} acknowledged by {operator}", operator, incident_id, inc.get("zone"))
            return inc
    raise HTTPException(status_code=404, detail="Incident not found")

@router.post("/{incident_id}/assign")
def assign_response_team(incident_id: str, payload: Dict[str, Any] = Body(...)):
    team_id = payload.get("team_id", "RES-01")
    operator = payload.get("operator", "DISASTER_COMMANDER")
    for inc in twin_state_manager.incidents:
        if inc["id"] == incident_id:
            inc["assigned_team"] = team_id
            inc["status"] = "RESPONSE_ASSIGNED"
            res = evacuation_manager.assign_resource(team_id, incident_id)
            disaster_state_machine.transition_to("RESPONSE", f"Assigned {team_id} to Incident {incident_id}", operator, incident_id, inc.get("zone"))
            return {"incident": inc, "resource": res}
    raise HTTPException(status_code=404, detail="Incident not found")

@router.post("/{incident_id}/evacuate")
def trigger_zone_evacuation(incident_id: str, payload: Dict[str, Any] = Body(default={})):
    zone_id = payload.get("zone_id", "ZONE_B")
    state = evacuation_manager.trigger_evacuation(zone_id)
    zone_manager.update_zone_status(zone_id, "CRITICAL", 3, "EVACUATE")
    return {"status": "EVACUATION_INITIATED", "zone": zone_id, "evacuation_state": state}

@router.post("/{incident_id}/resolve")
def resolve_incident(incident_id: str, payload: Dict[str, Any] = Body(default={})):
    operator = payload.get("operator", "DISASTER_COMMANDER")
    target_inc = None
    for inc in twin_state_manager.incidents:
        if inc["id"] == incident_id:
            inc["status"] = "CLOSED"
            inc["resolution"] = payload.get("resolution", "Zone hazard neutralized & safety verified.")
            target_inc = inc
            break

    if not target_inc:
        target_inc = {"id": incident_id, "zone": "ZONE_B", "disaster_type": "FIRE_SMOKE_HAZARD", "severity": "CRITICAL"}

    disaster_state_machine.transition_to("STABILIZATION", f"Incident {incident_id} stabilized", operator, incident_id, target_inc.get("zone"))
    disaster_state_machine.transition_to("RECOVERY", f"Incident {incident_id} recovery started", operator, incident_id, target_inc.get("zone"))
    disaster_state_machine.transition_to("RESOLVED", f"Incident {incident_id} resolved", operator, incident_id, target_inc.get("zone"))
    
    zone_manager.update_zone_status(target_inc.get("zone", "ZONE_B"), "NORMAL", 0, "SAFE")
    evacuation_manager.reset_evacuation()
    twin_state_manager.alarm_active = False
    twin_state_manager.is_interlocked = False

    report = post_disaster_engine.generate_recovery_report(target_inc, disaster_state_machine.state_history)
    return {"incident": target_inc, "report": report}

@router.get("/{incident_id}/report")
def get_incident_report(incident_id: str):
    target_inc = {"id": incident_id, "zone": "ZONE_B", "disaster_type": "FIRE_SMOKE_HAZARD", "severity": "CRITICAL"}
    for inc in twin_state_manager.incidents:
        if inc["id"] == incident_id:
            target_inc = inc
            break
    report = post_disaster_engine.generate_recovery_report(target_inc, disaster_state_machine.state_history)
    return report
