"""
Sentinel-X Open Source Satellite Ground Station & Telemetry Router
===================================================================
Provides REST API endpoints for:
  - SatNOGS Network & Libre Space ground station status
  - Orbital satellite pass predictions and azimuth/elevation rotor tracking
  - Open satellite space-segment emergency uplink bursts
  - Downlink frame telemetry inspection
  - Custom open-source satellite backend server URL configuration
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.services.satellite_service import (
    open_satellite_service,
    SatelliteGroundStationStatus,
    SatellitePass,
    SatelliteFrame
)

router = APIRouter(prefix="/api/v1/satellite", tags=["Open Source Satellite Ground Station"])

class SatelliteUplinkRequest(BaseModel):
    risk_score: float = Field(default=98.0, description="Risk score 0-100")
    motor_temp: Optional[float] = Field(default=84.0, description="Temperature parameter")
    vibration: Optional[float] = Field(default=2.4, description="Vibration parameter")
    source: str = Field(default="RPI5-EDGE-01", description="Emergency beacon origin")
    priority: str = Field(default="CRITICAL", description="Uplink priority")

class SatelliteServerConfigRequest(BaseModel):
    server_url: Optional[str] = Field(default=None, description="Open source satellite backend URL e.g. https://network.satnogs.org/api or local ground station http://127.0.0.1:5000")
    backend_server_url: Optional[str] = Field(default=None, description="Alias for server_url")

@router.get("/status", response_model=SatelliteGroundStationStatus)
def get_ground_station_status():
    """Returns the live connection state of the Open Source Satellite Ground Station."""
    return open_satellite_service.get_ground_station_status()

@router.get("/passes", response_model=List[SatellitePass])
def get_upcoming_satellite_passes():
    """Returns upcoming SatNOGS / TinyGS / Amateur satellite passes and tracking countdowns."""
    return open_satellite_service.get_upcoming_passes()

@router.get("/telemetry", response_model=List[SatelliteFrame])
def get_downlink_telemetry(limit: int = Query(20, ge=1, le=100)):
    """Returns received open-source satellite frames and decoded packet payloads."""
    return open_satellite_service.get_recent_frames(limit=limit)

@router.post("/uplink")
def transmit_emergency_satellite_uplink(req: SatelliteUplinkRequest):
    """Encodes and transmits an emergency packet over the open-source satellite network."""
    return open_satellite_service.transmit_emergency_uplink(req.dict())

@router.post("/connect")
def connect_satellite_link():
    """Establishes instantaneous live link to the active satellite constellation."""
    return open_satellite_service.connect_link()

@router.post("/disconnect")
def disconnect_satellite_link():
    """Disconnects space telemetry link and parks ground station rotor."""
    return open_satellite_service.disconnect_link()

@router.post("/config")
def configure_satellite_backend_server(req: SatelliteServerConfigRequest):
    """Connects or updates the remote open-source satellite backend server URL."""
    target_url = req.server_url or req.backend_server_url or "https://network.satnogs.org/api"
    return open_satellite_service.set_server_url(target_url)

