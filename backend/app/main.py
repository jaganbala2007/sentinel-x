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
Version: 1.0.0
License: MIT
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import alerts, sensors, machine
from app.core.config import settings

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Sentinel-X Core API",
    description=(
        "Enterprise REST + WebSocket API for the Sentinel-X Cognitive Safety "
        "Operating System. Provides real-time telemetry ingestion, alert "
        "distribution, PLC machine lockout, and Digital Twin state management."
    ),
    version="1.0.0",
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

# ---------------------------------------------------------------------------
# Health & Meta Endpoints
# ---------------------------------------------------------------------------


@app.get("/", tags=["Meta"], summary="API Root")
async def root() -> dict:
    """Returns API metadata and health confirmation."""
    return {
        "service": "Sentinel-X Core API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


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
