"""
Sentinel-X API Test Suite
==========================
Automated pytest tests for all FastAPI backend endpoints.

Run:
    pip install pytest pytest-asyncio httpx
    pytest tests/ -v --tb=short
"""

import pytest
from httpx import AsyncClient, ASGITransport

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app


# ---------------------------------------------------------------------------
# Test Client Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Meta / Health Tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_root_returns_metadata(client):
    """GET / should return service metadata."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Sentinel-X Core API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"


@pytest.mark.anyio
async def test_health_check_returns_200(client):
    """GET /health should return 200 with mesh status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["mesh_nodes_online"] == 1024
    assert data["ai_agents_active"] == 4


# ---------------------------------------------------------------------------
# Alerts Endpoint Tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_get_active_alerts(client):
    """GET /api/v1/alerts/active should return alert list."""
    response = await client.get("/api/v1/alerts/active")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert "total" in data
    assert isinstance(data["alerts"], list)


@pytest.mark.anyio
async def test_get_active_alerts_severity_filter(client):
    """GET /api/v1/alerts/active?severity=CRITICAL should filter correctly."""
    response = await client.get("/api/v1/alerts/active?severity=CRITICAL")
    assert response.status_code == 200
    data = response.json()
    for alert in data["alerts"]:
        assert alert["severity"] == "CRITICAL"


@pytest.mark.anyio
async def test_get_alert_history(client):
    """GET /api/v1/alerts/history should return paginated results."""
    response = await client.get("/api/v1/alerts/history?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert len(data["alerts"]) <= 10


@pytest.mark.anyio
async def test_get_alert_by_id(client):
    """GET /api/v1/alerts/{id} should return the correct alert."""
    response = await client.get("/api/v1/alerts/alert-942861")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "alert-942861"
    assert "severity" in data
    assert "details" in data


@pytest.mark.anyio
async def test_get_alert_not_found(client):
    """GET /api/v1/alerts/{nonexistent_id} should return 404."""
    response = await client.get("/api/v1/alerts/nonexistent-id-99999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_acknowledge_alert(client):
    """POST /api/v1/alerts/acknowledge should acknowledge an alert."""
    response = await client.post(
        "/api/v1/alerts/acknowledge",
        params={"alert_id": "alert-942861", "operator_id": "admin@sentinel.x"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "acknowledged"
    assert data["alert_id"] == "alert-942861"


# ---------------------------------------------------------------------------
# Sensors / Telemetry Tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_get_telemetry_snapshot(client):
    """GET /api/v1/sensors/telemetry should return full snapshot."""
    response = await client.get("/api/v1/sensors/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "nodes_synced" in data
    assert data["nodes_synced"] == 1024
    assert "gas_levels" in data
    assert "active_worker_count" in data
    assert 0.0 <= data["risk_score_global"] <= 100.0


@pytest.mark.anyio
async def test_get_worker_profiles(client):
    """GET /api/v1/sensors/workers should return worker Digital DNA list."""
    response = await client.get("/api/v1/sensors/workers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    worker = data[0]
    assert "worker_id" in worker
    assert "heart_rate_bpm" in worker
    assert "fatigue_coefficient" in worker
    assert 0.0 <= worker["fatigue_coefficient"] <= 1.0


@pytest.mark.anyio
async def test_ingest_sensor_reading_normal(client):
    """POST /api/v1/sensors/ingest should accept a normal sensor reading."""
    payload = {
        "sensor_id": "CO2_SENSOR_TEST_001",
        "sensor_type": "co2",
        "value": 350.0,
        "unit": "ppm",
        "zone": "Zone-A",
        "is_anomaly": False
    }
    response = await client.post("/api/v1/sensors/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ingested"
    assert data["is_anomaly"] is False


@pytest.mark.anyio
async def test_ingest_sensor_reading_anomaly_detected(client):
    """POST /api/v1/sensors/ingest should auto-detect anomaly on threshold breach."""
    payload = {
        "sensor_id": "CO2_SENSOR_TEST_002",
        "sensor_type": "co2",
        "value": 1500.0,   # Well above 800 ppm threshold
        "unit": "ppm",
        "zone": "Zone-B",
        "is_anomaly": False
    }
    response = await client.post("/api/v1/sensors/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_anomaly"] is True


# ---------------------------------------------------------------------------
# Machine Control Tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_get_machine_status(client):
    """GET /api/v1/machine/status should list all registered machines."""
    response = await client.get("/api/v1/machine/status")
    assert response.status_code == 200
    data = response.json()
    assert "machines" in data
    assert len(data["machines"]) > 0
    machine = data["machines"][0]
    assert "machine_id" in machine
    assert "status" in machine


@pytest.mark.anyio
async def test_machine_lockout_success(client):
    """POST /api/v1/machine/lockout should successfully lock out a machine."""
    payload = {
        "machine_id": "PLC_BOILER_A",
        "operator_id": "admin@sentinel.x",
        "reason": "Automated test lockout",
        "emergency_override": False
    }
    response = await client.post("/api/v1/machine/lockout", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "PLC_BOILER_A" in data["locked_units"]
    assert data["latency_ms"] > 0


@pytest.mark.anyio
async def test_machine_lockout_not_found(client):
    """POST /api/v1/machine/lockout with unknown machine should return 404."""
    payload = {
        "machine_id": "PLC_NONEXISTENT_99",
        "operator_id": "admin@sentinel.x",
        "reason": "Test",
        "emergency_override": False
    }
    response = await client.post("/api/v1/machine/lockout", json=payload)
    assert response.status_code == 404


@pytest.mark.anyio
async def test_machine_restore(client):
    """POST /api/v1/machine/restore should restore a locked machine."""
    # First lock a machine
    await client.post("/api/v1/machine/lockout", json={
        "machine_id": "PLC_CONVEYOR_01",
        "operator_id": "admin@sentinel.x",
        "reason": "Setup for restore test",
        "emergency_override": True
    })
    # Now restore it
    response = await client.post(
        "/api/v1/machine/restore",
        params={"machine_id": "PLC_CONVEYOR_01", "operator_id": "admin@sentinel.x"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "restored"
