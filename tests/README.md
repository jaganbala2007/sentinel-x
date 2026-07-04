# Sentinel-X Tests

Automated test suite for the Sentinel-X backend API.

## Test Coverage

| Module | Tests | Coverage |
|---|---|---|
| Health / Meta | 2 | Root endpoint, health probe |
| Alerts API | 5 | Active list, filter, history, get by ID, acknowledge |
| Sensors API | 4 | Telemetry snapshot, worker profiles, ingest (normal + anomaly) |
| Machine API | 4 | Status list, lockout, lockout 404, restore |
| **Total** | **15** | All public REST endpoints |

## Running Tests

```bash
# Install test dependencies
cd backend
pip install -r requirements.txt
pip install pytest pytest-asyncio anyio

# Run all tests
pytest ../tests/ -v --tb=short

# Run with coverage report
pip install pytest-cov
pytest ../tests/ -v --cov=app --cov-report=html

# Run specific test
pytest ../tests/test_api.py::test_health_check_returns_200 -v
```

## Test Output Example

```
tests/test_api.py::test_root_returns_metadata              PASSED
tests/test_api.py::test_health_check_returns_200           PASSED
tests/test_api.py::test_get_active_alerts                  PASSED
tests/test_api.py::test_get_active_alerts_severity_filter  PASSED
tests/test_api.py::test_get_alert_history                  PASSED
tests/test_api.py::test_get_alert_by_id                    PASSED
tests/test_api.py::test_get_alert_not_found                PASSED
tests/test_api.py::test_acknowledge_alert                  PASSED
tests/test_api.py::test_get_telemetry_snapshot             PASSED
tests/test_api.py::test_get_worker_profiles                PASSED
tests/test_api.py::test_ingest_sensor_reading_normal       PASSED
tests/test_api.py::test_ingest_sensor_reading_anomaly      PASSED
tests/test_api.py::test_get_machine_status                 PASSED
tests/test_api.py::test_machine_lockout_success            PASSED
tests/test_api.py::test_machine_lockout_not_found          PASSED
tests/test_api.py::test_machine_restore                    PASSED
============================== 16 passed in 0.94s ==============================
```

## Test Structure

```
tests/
├── test_api.py         # Full REST API endpoint tests
├── conftest.py         # Shared fixtures (planned)
├── test_schemas.py     # Pydantic model validation tests (planned)
└── README.md
```

## Adding New Tests

Follow the existing pattern using `@pytest.mark.anyio` and the async `client` fixture:

```python
@pytest.mark.anyio
async def test_my_new_endpoint(client):
    response = await client.get("/api/v1/my-endpoint")
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```
