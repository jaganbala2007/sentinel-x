"""
Communication Resilience Subsystem Router
"""

from fastapi import APIRouter
from app.schemas.disaster import CommsStatusSchema
from app.services.communication_manager import communication_manager

router = APIRouter(prefix="/api/v1/communications", tags=["Communication Resilience"])

@router.get("/status", response_model=CommsStatusSchema)
def get_comms_status():
    return communication_manager.get_status()

@router.post("/set-mode/{mode}")
def set_comms_mode(mode: str):
    communication_manager.set_mode(mode.upper())
    return communication_manager.get_status()
