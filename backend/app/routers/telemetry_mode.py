"""
Sentinel-X Telemetry Mode & Simulation API Router
=================================================
Provides endpoints for:
  - Data Source Selection (ONLINE vs OFFLINE)
  - Digital Twin Simulation Control (Start, Pause, Reset, Scenarios, Speed, Seed)
  - Unified Normalized Sensor Telemetry (Node 1, Node 2)
  - MQTT Edge Ingestion for Physical Hardware (ESP32 Nodes)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from app.core.telemetry_provider import (
    telemetry_manager,
    SystemTelemetrySnapshot,
    NodeTelemetry,
    SimulationScenario
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Request/Response Schemas
# ---------------------------------------------------------------------------

class ModeSelectRequest(BaseModel):
    mode: str = Field(..., description="'ONLINE' or 'OFFLINE'")


class SimulationControlRequest(BaseModel):
    action: str = Field("start", description="'start', 'pause', 'resume', 'reset'")
    scenario: Optional[str] = Field(None, description="Scenario name")
    speed: Optional[float] = Field(None, description="Speed multiplier (0.5, 1.0, 2.0, 5.0, 10.0)")
    duration: Optional[float] = Field(None, description="Demo duration in seconds")
    seed: Optional[int] = Field(None, description="Deterministic random seed")


class IngestLiveTelemetryRequest(BaseModel):
    node_id: str = Field(..., description="e.g. 'SX-NODE-01' or 'SX-NODE-02'")
    zone: str = Field(..., description="e.g. 'ZONE-1' or 'ZONE-2'")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative Humidity in percentage")
    mq135_raw: int = Field(..., description="MQ-135 raw ADC index (0-4095)")
    accel_x: Optional[float] = Field(0.0, description="ADXL345 X-axis")
    accel_y: Optional[float] = Field(0.0, description="ADXL345 Y-axis")
    accel_z: Optional[float] = Field(9.81, description="ADXL345 Z-axis")
    vibration_hz: Optional[float] = Field(2.1, description="Vibration frequency Hz")


# ---------------------------------------------------------------------------
# Mode Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "/mode",
    summary="Get Current Operational Telemetry Mode",
    description="Returns whether the application is running in ONLINE (Physical ESP32 MQTT) or OFFLINE (Digital Twin Simulation) mode."
)
async def get_mode() -> Dict[str, Any]:
    sim = telemetry_manager.simulation_engine
    return {
        "mode": telemetry_manager.mode,
        "data_source_label": "LIVE SENSOR DATA" if telemetry_manager.mode == "ONLINE" else "DIGITAL TWIN SIMULATION",
        "simulation": {
            "running": sim.running,
            "paused": sim.paused,
            "scenario": sim.scenario,
            "speed": sim.speed,
            "duration": sim.duration,
            "elapsed_seconds": round(sim.elapsed_sim_time, 1),
            "seed": sim.seed,
            "available_scenarios": [
                SimulationScenario.NORMAL,
                SimulationScenario.HIGH_TEMP,
                SimulationScenario.AIR_QUALITY,
                SimulationScenario.VIBRATION_ANOMALY,
                SimulationScenario.MULTI_SENSOR,
                SimulationScenario.CUSTOM,
            ]
        }
    }


@router.post(
    "/mode/select",
    summary="Select Operational Telemetry Mode",
    description="Switches data source between ONLINE (Physical ESP32 Nodes) and OFFLINE (Digital Twin Simulation)."
)
async def select_mode(req: ModeSelectRequest) -> Dict[str, Any]:
    try:
        res = telemetry_manager.set_mode(req.mode)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/simulation/control",
    summary="Control Digital Twin Simulation Engine",
    description="Control playback, switch scenarios, modify speed, and set deterministic seeds."
)
async def control_simulation(req: SimulationControlRequest) -> Dict[str, Any]:
    sim = telemetry_manager.simulation_engine

    if req.seed is not None:
        sim.reset(new_seed=req.seed)

    if req.scenario:
        dur = req.duration or sim.duration
        sim.set_scenario(req.scenario, duration=dur)

    if req.speed is not None:
        sim.set_speed(req.speed)

    action = req.action.lower().strip()
    if action == "start":
        sim.running = True
        sim.paused = False
    elif action == "pause":
        sim.paused = True
    elif action == "resume":
        sim.paused = False
    elif action == "reset":
        sim.reset()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action '{action}'")

    return {
        "status": "success",
        "action": action,
        "scenario": sim.scenario,
        "speed": sim.speed,
        "paused": sim.paused,
        "elapsed_seconds": round(sim.elapsed_sim_time, 1),
        "seed": sim.seed
    }


# ---------------------------------------------------------------------------
# Telemetry Snapshot & Node Query Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "/telemetry/current",
    response_model=SystemTelemetrySnapshot,
    summary="Get Unified System Telemetry Snapshot",
    description="Returns current normalized telemetry for Node 1 and Node 2 from the active data source."
)
async def get_current_telemetry() -> SystemTelemetrySnapshot:
    return telemetry_manager.get_current_snapshot()


@router.get(
    "/telemetry/history",
    summary="Get Telemetry History with Source Metadata",
    description="Query historical telemetry recordings stamped with LIVE or SIMULATION source labels."
)
async def get_telemetry_history(
    node_id: Optional[str] = Query(None, description="Filter by node ID"),
    data_source: Optional[str] = Query(None, description="'LIVE' or 'SIMULATION'"),
    limit: int = Query(50, ge=1, le=500)
):
    history = telemetry_manager.get_history(node_id=node_id, data_source=data_source, limit=limit)
    return {
        "count": len(history),
        "data_source_filter": data_source or "ALL",
        "readings": history
    }


@router.post(
    "/telemetry/ingest",
    response_model=NodeTelemetry,
    summary="Ingest Physical ESP32 Node Telemetry",
    description="Receives real sensor telemetry from ESP32 Node 1 or Node 2 via MQTT / Raspberry Pi 4 gateway."
)
async def ingest_telemetry(payload: IngestLiveTelemetryRequest) -> NodeTelemetry:
    res = telemetry_manager.ingest_live_reading(payload.dict())
    return res
