"""
Sentinel-X Hazard Zone Mapping REST API Router
===============================================
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from app.services.zone_manager import zone_manager

router = APIRouter(prefix="/api/v1/zones", tags=["Hazard Zones"])

@router.get("")
def get_zones():
    return zone_manager.get_all_zones()

@router.post("/{zone_id}/status")
def update_zone_status(zone_id: str, payload: Dict[str, Any] = Body(...)):
    status = payload.get("status", "NORMAL")
    hazard_level = payload.get("hazardLevel", 0)
    evac_status = payload.get("evacuationStatus", None)
    zone = zone_manager.update_zone_status(zone_id, status, hazard_level, evac_status)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone
