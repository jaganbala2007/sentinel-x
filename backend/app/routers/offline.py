"""
Offline Store-and-Forward & Batch Synchronization Router
"""

from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.store_and_forward import store_and_forward_service

router = APIRouter(prefix="/api/v1/offline", tags=["Offline Store & Forward"])

@router.get("/events")
def get_pending_offline_events():
    return store_and_forward_service.get_pending_events()

@router.post("/sync")
def trigger_batch_synchronization():
    return store_and_forward_service.sync_all_pending()

@router.post("/queue-test")
def queue_test_offline_event():
    evt_id = store_and_forward_service.queue_event(
        node_id="NODE-02",
        event_type="DISASTER_ALERT",
        severity="CRITICAL",
        risk_score=84,
        confidence=94,
        payload={"stage_m": 3.85, "rate_m_min": 0.08, "siren": "ACTIVE"}
    )
    return {"status": "QUEUED", "event_id": evt_id}
