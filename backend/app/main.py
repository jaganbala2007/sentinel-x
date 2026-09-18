"""
Sentinel-X FastAPI Backend — Disaster Intelligence & Emergency Command
======================================================================
Primary REST + WebSocket API server for Sentinel-X.
Ground-truth edge services for:
  - Distributed ESP32 (Node-01, Node-02) sensor telemetry ingestion
  - Explainable Sensor Trust & Byzantine Quarantine Engine
  - Authoritative Digital Twin State (GET /api/v1/twin/state)
  - Mosquitto MQTT Integration (1883)
  - Fault Simulation & Emergency Interlock Controllers
  - Live WebSocket telemetry broadcasting to EOC Cockpit

Author: Sentinel-X Principal Engineering Team
Version: 2.5.0
License: MIT
"""

import sys
import os
import asyncio
import json
import time
from typing import Dict, Any, Optional

# Ensure 'backend' directory and workspace root are on sys.path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
_workspace_root = os.path.dirname(_backend_dir)
if _workspace_root not in sys.path:
    sys.path.insert(0, _workspace_root)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.services.twin_state_manager import twin_state_manager
from app.services.mqtt_service import mqtt_service
from app.routers import telemetry, disasters, sensors, communications, offline, simulation, system, environment, sih_demo, incidents, zones, satellite, metrology, digital_twins, alerts, machine, telemetry_mode, cyber_twins_v3

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Mission-critical REST + WebSocket API for the Sentinel-X Quantum-Resilient "
        "Autonomous Disaster Intelligence & Emergency Communication Platform. "
        "Operates on distributed ESP32 sensing, Raspberry Pi edge intelligence, "
        "Mosquitto MQTT (1883), and local SQLite store-and-forward."
    ),
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(system.router)
app.include_router(telemetry.router)
app.include_router(disasters.router)
app.include_router(sensors.router)
app.include_router(communications.router)
app.include_router(offline.router)
app.include_router(simulation.router)
app.include_router(environment.router)
app.include_router(sih_demo.router)
app.include_router(incidents.router)
app.include_router(zones.router)
app.include_router(satellite.router)
app.include_router(metrology.router)
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(machine.router, prefix="/api/v1/machine", tags=["Machine Lockout"])
app.include_router(telemetry_mode.router, prefix="/api/v1/telemetry-mode", tags=["Telemetry Mode"])
app.include_router(cyber_twins_v3.router, prefix="/api/v1/cyber-twins", tags=["Cyber Twins v3"])
app.include_router(digital_twins.router, prefix="/api/v1/digital-twins", tags=["Digital Twins"])

# ---------------------------------------------------------------------------
# Static Web Assets Mounting
# ---------------------------------------------------------------------------

_frontend_dir = os.path.join(_workspace_root, "frontend")
_assets_dir = os.path.join(_workspace_root, "assets")

if os.path.isdir(_frontend_dir):
    app.mount("/frontend", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
if os.path.isdir(_assets_dir):
    app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")

# ---------------------------------------------------------------------------
# Authoritative Endpoints (Section 6 & 7)
# ---------------------------------------------------------------------------

@app.get("/")
def root_endpoint():
    landing_file = os.path.join(_workspace_root, "index.html")
    if os.path.isfile(landing_file):
        return FileResponse(landing_file)
    return twin_state_manager.get_authoritative_state()

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Sentinel-X Edge Engine",
        "systemMode": twin_state_manager.system_mode,
        "mqtt": twin_state_manager.mqtt_status,
        "edge_node": "RPI3-EDGE-01",
        "storage": "SQLite WAL Buffer Active",
        "timestamp": int(time.time())
    }

@app.get("/api/v1/twin/state")
def get_authoritative_twin_state():
    """Authoritative combined Sentinel-X state for UI (Section 7)."""
    return twin_state_manager.get_authoritative_state()

@app.post("/api/v1/telemetry")
def ingest_http_telemetry(payload: Dict[str, Any] = Body(...)):
    """HTTP Telemetry Ingestion endpoint."""
    node_id = str(payload.get("node_id", payload.get("nodeId", ""))).upper()
    if "01" in node_id or "NODE1" in node_id:
        twin_state_manager.update_node1(payload)
    elif "02" in node_id or "NODE2" in node_id:
        twin_state_manager.update_node2(payload)
    else:
        raise HTTPException(status_code=400, detail="Invalid node_id in telemetry payload.")
    return {"status": "INGESTED", "node": node_id, "state": twin_state_manager.get_authoritative_state()}

@app.post("/api/v1/safety/interlock")
def trigger_safety_interlock():
    twin_state_manager.is_interlocked = True
    twin_state_manager.alarm_active = True
    twin_state_manager.risk_level = "CRITICAL"
    twin_state_manager.safety_decision = "ISOLATE"
    return twin_state_manager.get_authoritative_state()

@app.post("/api/v1/system/recover")
def recover_system():
    return twin_state_manager.recover()

@app.post("/api/v1/fault/{fault_type}")
def inject_fault(fault_type: str):
    if fault_type not in ["spoof", "comms", "power", "hazard"]:
        raise HTTPException(status_code=400, detail=f"Unknown fault type: {fault_type}")
    return twin_state_manager.inject_fault(fault_type)

@app.post("/api/v1/communication/isolate")
def isolate_communication():
    twin_state_manager.comm_state = "ISOLATED"
    twin_state_manager.active_channel = "BLACKBOX_WAL"
    return twin_state_manager.get_authoritative_state()

@app.get("/api/v1/communication/status")
def get_communication_status():
    return {
        "commState": twin_state_manager.comm_state,
        "activeChannel": twin_state_manager.active_channel,
        "mqtt": twin_state_manager.mqtt_status,
        "tier1_lan": "ONLINE",
        "tier2_hf": "READY (7.105 MHz AX.25)",
        "tier3_satellite": "ADAPTER READY",
        "tier4_wal_buffer": "ARMED"
    }

@app.post("/api/v1/communication/recover")
def recover_communication():
    twin_state_manager.comm_state = "NORMAL"
    twin_state_manager.active_channel = "INTERNET"
    return twin_state_manager.get_authoritative_state()

@app.get("/api/v1/storage/status")
def get_storage_status():
    return {
        "storage": "LOCAL_SQLITE_WAL",
        "bufferStatus": "ARMED",
        "databaseFile": "sentinel_edge.db",
        "persistedEventsCount": len(twin_state_manager.audit_log),
        "incidentsCount": len(twin_state_manager.incidents),
        "freeSpaceMB": 12400
    }

@app.get("/api/v1/incidents")
def get_incidents():
    return {
        "total": len(twin_state_manager.incidents),
        "incidents": twin_state_manager.incidents
    }

# ---------------------------------------------------------------------------
# WebSocket Telemetry Broadcast Channel
# ---------------------------------------------------------------------------

class TelemetryConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = TelemetryConnectionManager()

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.8)
            state = twin_state_manager.get_authoritative_state()
            await websocket.send_text(json.dumps(state))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# ---------------------------------------------------------------------------
# Lifecycle Events
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    init_db()
    mqtt_service.start()

@app.on_event("shutdown")
def on_shutdown():
    mqtt_service.stop()
