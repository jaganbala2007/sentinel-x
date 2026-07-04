# Sentinel-X Backend

FastAPI REST + WebSocket API server for the Sentinel-X Cognitive Safety OS.

## Overview

The backend provides:
- **REST API** — Alert management, sensor telemetry, machine control
- **WebSocket Streaming** — Real-time telemetry push to cockpit dashboard
- **Error Logging** — Client-side error reception from frontend
- **Health Endpoints** — Kubernetes liveness/readiness probes

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app factory, middleware, route registration
│   ├── core/
│   │   └── config.py        # Pydantic Settings — all env vars here
│   ├── models/
│   │   └── schemas.py       # Pydantic v2 request/response DTOs
│   └── routers/
│       ├── alerts.py        # GET/POST /api/v1/alerts/*
│       ├── sensors.py       # GET/POST /api/v1/sensors/*
│       └── machine.py       # POST /api/v1/machine/lockout
├── requirements.txt         # Python dependencies
├── Dockerfile               # Multi-stage production Docker image
├── .env.example             # Environment variable template
└── README.md
```

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**API Documentation:** http://localhost:8080/docs  
**ReDoc:** http://localhost:8080/redoc

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check (Kubernetes probe) |
| `GET` | `/api/v1/alerts/active` | Active alerts list |
| `GET` | `/api/v1/alerts/{id}` | Single alert by ID |
| `POST` | `/api/v1/alerts/acknowledge` | Acknowledge an alert |
| `GET` | `/api/v1/sensors/telemetry` | Aggregated sensor snapshot |
| `GET` | `/api/v1/sensors/workers` | Worker Digital DNA profiles |
| `POST` | `/api/v1/sensors/ingest` | Ingest sensor reading from edge |
| `POST` | `/api/v1/machine/lockout` | Emergency PLC machine lockout |
| `GET` | `/api/v1/machine/status` | All machine states |
| `POST` | `/api/v1/machine/restore` | Restore locked machine |

## Docker

```bash
# Build image
docker build -t sentinelx-backend .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  sentinelx-backend
```

## Environment Variables

See [`.env.example`](.env.example) for full configuration reference.

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pydantic` + `pydantic-settings` | Data validation + config |
| `asyncpg` + `sqlalchemy` | Async PostgreSQL |
| `redis` | Telemetry cache |
| `paho-mqtt` | MQTT sensor ingestion |
| `pymodbus` | PLC Modbus/TCP control |
| `onnxruntime` | On-server AI inference |

## Testing

```bash
pip install pytest pytest-asyncio
pytest ../tests/ -v
```
