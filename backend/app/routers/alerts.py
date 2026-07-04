"""
Alerts Router
=============
REST API endpoints for safety alert management.

Endpoints:
    GET  /api/v1/alerts/active      — List all active (unacknowledged) alerts
    GET  /api/v1/alerts/{alert_id}  — Retrieve a specific alert by ID
    POST /api/v1/alerts/acknowledge — Acknowledge an alert
    GET  /api/v1/alerts/history     — Paginated 24h alert history
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.schemas import AlertSchema, AlertSeverity, AlertListResponse, AlertTriggerSource

router = APIRouter()

# ---------------------------------------------------------------------------
# Mock data — replace with real database queries in production
# ---------------------------------------------------------------------------

_MOCK_ALERTS: List[AlertSchema] = [
    AlertSchema(
        id="alert-942861",
        timestamp=datetime(2026, 7, 1, 15, 43, 9),
        severity=AlertSeverity.WARNING,
        trigger_source=AlertTriggerSource.VISION_AI,
        zone="Zone-B",
        details="Worker John Doe detected crossing restricted compressor zone boundary.",
        worker_id="worker-john-doe-01",
        acknowledged=False,
    ),
    AlertSchema(
        id="alert-942800",
        timestamp=datetime(2026, 7, 1, 15, 33, 54),
        severity=AlertSeverity.INFO,
        trigger_source=AlertTriggerSource.SENSOR_THRESHOLD,
        zone="Zone-A",
        details="Sentinel-X Cognitive mesh initialized. All 1024 edge nodes synchronized.",
        acknowledged=True,
        acknowledged_by="admin@sentinel.x",
    ),
]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/active",
    response_model=AlertListResponse,
    summary="Get Active Alerts",
    description="Returns all unacknowledged safety alerts across all factory zones.",
)
async def get_active_alerts(
    severity: Optional[AlertSeverity] = Query(None, description="Filter by severity level"),
    zone: Optional[str] = Query(None, description="Filter by factory zone"),
) -> AlertListResponse:
    """
    Returns all currently active (unacknowledged) safety alerts.

    Optionally filter by severity or zone.
    In production, this queries the PostgreSQL alerts table with Redis caching.
    """
    active = [a for a in _MOCK_ALERTS if not a.acknowledged]

    if severity:
        active = [a for a in active if a.severity == severity]
    if zone:
        active = [a for a in active if a.zone == zone]

    return AlertListResponse(total=len(active), alerts=active)


@router.get(
    "/history",
    response_model=AlertListResponse,
    summary="Get Alert History (24h)",
    description="Returns paginated alert history for the last 24 hours.",
)
async def get_alert_history(
    limit: int = Query(50, le=200, description="Maximum records to return"),
    offset: int = Query(0, description="Pagination offset"),
) -> AlertListResponse:
    """
    Returns paginated alert history.
    Sorted newest-first by default.
    """
    paginated = _MOCK_ALERTS[offset: offset + limit]
    return AlertListResponse(total=len(_MOCK_ALERTS), alerts=paginated)


@router.get(
    "/{alert_id}",
    response_model=AlertSchema,
    summary="Get Alert by ID",
)
async def get_alert(alert_id: str) -> AlertSchema:
    """Retrieves a specific alert event by its unique identifier."""
    for alert in _MOCK_ALERTS:
        if alert.id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")


@router.post(
    "/acknowledge",
    response_model=dict,
    summary="Acknowledge an Alert",
)
async def acknowledge_alert(
    alert_id: str,
    operator_id: str,
) -> dict:
    """
    Marks an alert as acknowledged by an operator.
    Requires the alert ID and the operator's email.
    """
    for alert in _MOCK_ALERTS:
        if alert.id == alert_id:
            if alert.acknowledged:
                raise HTTPException(
                    status_code=409,
                    detail=f"Alert '{alert_id}' is already acknowledged.",
                )
            alert.acknowledged = True
            alert.acknowledged_by = operator_id
            return {
                "status": "acknowledged",
                "alert_id": alert_id,
                "operator": operator_id,
                "timestamp": datetime.utcnow().isoformat(),
            }

    raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")
