"""
Sensor Fleet & Trust Scoring Router
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.disaster import SensorTrustSchema
from app.services.sensor_trust_engine import sensor_trust_engine

router = APIRouter(prefix="/api/v1/sensors", tags=["Sensor Fleet & Trust"])

@router.get("/trust", response_model=List[SensorTrustSchema])
def get_sensor_trust_matrix():
    return sensor_trust_engine.get_all_trust_states()

@router.get("/{node_id}/trust", response_model=SensorTrustSchema)
def get_node_trust(node_id: str):
    states = {s.node_id: s for s in sensor_trust_engine.get_all_trust_states()}
    if node_id not in states:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return states[node_id]

@router.post("/{node_id}/quarantine")
def manually_quarantine_node(node_id: str):
    res = sensor_trust_engine.evaluate_node(node_id, current_stage=99.0, rate_of_rise=10.0, neighbor_readings=[2.41])
    return {"status": "QUARANTINED", "node_id": node_id, "trust_score": res.trust_score, "reasons": res.reasons}

@router.post("/{node_id}/reinstate")
def reinstate_node(node_id: str):
    res = sensor_trust_engine.evaluate_node(node_id, current_stage=2.41, rate_of_rise=0.01, neighbor_readings=[2.41])
    return {"status": "VERIFIED", "node_id": node_id, "trust_score": res.trust_score}
