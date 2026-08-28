"""
Sentinel-X FastAPI Backend
==========================
Primary REST + WebSocket API server for the Sentinel-X Cognitive Safety OS.

Exposes endpoints for:
  - Real-time alert ingestion and distribution
  - Sensor telemetry aggregation
  - Machine PLC lockout commands
  - Worker Digital DNA profile management
  - Risk field state queries
  - WebSocket streams for live cockpit UI updates

Author: Sentinel-X Engineering Team
Version: 1.1.0
License: MIT
"""

import sys
import os

# Ensure 'backend' directory is on sys.path so 'app.*' imports work from any working directory
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import alerts, sensors, machine, digital_twins, digital_twins_v3, cyber_twins_v3, telemetry_mode
from app.core.config import settings

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Sentinel-X Cyber-Resilient Industrial Digital Twin API",
    description=(
        "Enterprise REST + WebSocket API for the Sentinel-X Cyber-Resilient "
        "Industrial Digital Twin Platform. Provides real-time telemetry ingestion, "
        "sensor trust scoring, cyber integrity defense simulation, Worker/Machine "
        "Safety DNA, predictive machine life (RUL), What-If simulations, and AI Copilot."
    ),
    version="1.1.0",
    contact={
        "name": "Sentinel-X Engineering",
        "url": "https://github.com/jaganbala2007/sentinel-x",
        "email": "jaganbala2007@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS Middleware (allow cockpit UI to connect)
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Route Registration
# ---------------------------------------------------------------------------

app.include_router(
    alerts.router,
    prefix="/api/v1/alerts",
    tags=["Alerts"],
)

app.include_router(
    sensors.router,
    prefix="/api/v1/sensors",
    tags=["Sensors & Telemetry"],
)

app.include_router(
    machine.router,
    prefix="/api/v1/machine",
    tags=["Machine Control"],
)

app.include_router(
    digital_twins.router,
    prefix="/api/v1/digital-twins",
    tags=["Digital Twins & Reconstruction v1"],
)

app.include_router(
    digital_twins_v3.router,
    prefix="/api/v3/digital-twins",
    tags=["Digital Twins & Reconstruction v3"],
)

app.include_router(
    cyber_twins_v3.router,
    prefix="/api/v3",
    tags=["Cyber-Resilient Industrial Intelligence v3"],
)

app.include_router(
    telemetry_mode.router,
    prefix="/api/v1",
    tags=["Online / Offline Telemetry Mode & Simulation Engine"],
)

# ---------------------------------------------------------------------------
# Health & Meta Endpoints
# ---------------------------------------------------------------------------
# Health & Dashboard Endpoints
# ---------------------------------------------------------------------------

from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

_frontend_src_dir = os.path.join(os.path.dirname(_backend_dir), "frontend", "src")


_assets_dir = os.path.join(os.path.dirname(_backend_dir), "assets")


@app.get("/", tags=["Meta"], summary="API Root")
async def root() -> dict:
    """Returns API metadata and health confirmation."""
    return {
        "service": "Sentinel-X Core API",
        "version": "1.1.0",
        "status": "operational",
        "docs": "/docs",
        "dashboard": "/dashboard",
    }


@app.get("/dashboard", tags=["Dashboard"], summary="Open 3D Cockpit Dashboard")
@app.get("/app", tags=["Dashboard"], summary="Open 3D Cockpit Dashboard")
async def serve_dashboard():
    """Serves the 3D Digital Twin Cockpit UI application."""
    app_html = os.path.join(_frontend_src_dir, "app.html")
    if os.path.exists(app_html):
        return FileResponse(app_html)
    return HTMLResponse("<h1>Cockpit Dashboard app.html not found</h1>", status_code=404)


@app.get("/twin-engine.js", summary="Serve twin-engine.js")
async def serve_twin_engine():
    """Serves the client-side 3D Digital Twin & Reconstruction engine."""
    fpath = os.path.join(_frontend_src_dir, "twin-engine.js")
    if os.path.exists(fpath):
        return FileResponse(fpath, media_type="application/javascript")
    return HTMLResponse("Not Found", status_code=404)


if os.path.exists(_frontend_src_dir):
    app.mount("/static", StaticFiles(directory=_frontend_src_dir), name="static")
    app.mount("/src", StaticFiles(directory=_frontend_src_dir), name="src")

if os.path.exists(_assets_dir):
    app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")


@app.get("/health", tags=["Meta"], summary="Health Check")
async def health_check() -> JSONResponse:
    """
    Kubernetes/Docker liveness probe endpoint.
    Returns HTTP 200 if the service is alive.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "mesh_nodes_online": 1024,
            "ai_agents_active": 4,
        },
    )


@app.post("/api/log-error", tags=["Meta"], summary="Client Error Logger")
async def log_client_error(payload: dict) -> dict:
    """
    Receives client-side JavaScript errors from the cockpit dashboard
    and logs them server-side for debugging.

    Args:
        payload: JSON body containing error type, message, and details.

    Returns:
        Acknowledgment dict.
    """
    error_type = payload.get("type", "unknown")
    message = payload.get("message", "")
    details = payload.get("details", "")
    url = payload.get("url", "")

    # In production, route to centralized logging (e.g., Cloud Logging, Sentry)
    print(f"[CLIENT ERROR] [{error_type}] {message} | {details} | URL: {url}")

    return {"received": True, "type": error_type}
