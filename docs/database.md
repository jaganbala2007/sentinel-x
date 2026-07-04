# Sentinel-X Database Schema

## Overview

Sentinel-X uses **PostgreSQL 16** as the primary persistent data store, with **Redis 7** as a real-time telemetry cache layer.

---

## PostgreSQL Schema

### Table: `workers`
Stores permanent worker profiles and current Digital DNA safety state.

```sql
CREATE TABLE workers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id     VARCHAR(50) UNIQUE NOT NULL,
    full_name       VARCHAR(200) NOT NULL,
    role            VARCHAR(100) NOT NULL,
    department      VARCHAR(100),
    site_id         UUID REFERENCES sites(id),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `worker_vitals`
Time-series biometric readings from smart helmets and wearables.

```sql
CREATE TABLE worker_vitals (
    id                    BIGSERIAL PRIMARY KEY,
    worker_id             UUID NOT NULL REFERENCES workers(id),
    timestamp             TIMESTAMPTZ NOT NULL,
    heart_rate_bpm        SMALLINT,
    spo2_percent          NUMERIC(5,2),
    fatigue_coefficient   NUMERIC(4,3),   -- 0.000 → 1.000
    pos_x                 NUMERIC(8,3),   -- UWB position (meters)
    pos_y                 NUMERIC(8,3),
    pos_z                 NUMERIC(8,3),
    zone_id               VARCHAR(50),
    ppe_compliant         BOOLEAN,
    helmet_battery_pct    SMALLINT
) PARTITION BY RANGE (timestamp);

-- Monthly partitions (created automatically)
CREATE TABLE worker_vitals_2026_07 PARTITION OF worker_vitals
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

CREATE INDEX idx_worker_vitals_worker_time ON worker_vitals(worker_id, timestamp DESC);
```

### Table: `sensor_readings`
Time-series environmental and machine sensor data.

```sql
CREATE TABLE sensor_readings (
    id              BIGSERIAL PRIMARY KEY,
    sensor_id       VARCHAR(100) NOT NULL,
    sensor_type     VARCHAR(50) NOT NULL,   -- co2, h2s, temperature, vibration, noise
    value           NUMERIC(12,4) NOT NULL,
    unit            VARCHAR(20) NOT NULL,   -- ppm, celsius, Hz, dB
    zone_id         VARCHAR(50) NOT NULL,
    is_anomaly      BOOLEAN DEFAULT FALSE,
    timestamp       TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (timestamp);

CREATE INDEX idx_sensor_readings_sensor_time ON sensor_readings(sensor_id, timestamp DESC);
CREATE INDEX idx_sensor_readings_zone_type ON sensor_readings(zone_id, sensor_type);
```

### Table: `alerts`
Safety event log — immutable audit trail.

```sql
CREATE TABLE alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    severity        VARCHAR(20) NOT NULL CHECK (severity IN ('INFO','WARNING','CRITICAL')),
    trigger_source  VARCHAR(50) NOT NULL,
    zone_id         VARCHAR(50),
    worker_id       UUID REFERENCES workers(id),
    machine_id      VARCHAR(100),
    title           VARCHAR(500) NOT NULL,
    details         TEXT,
    is_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES workers(id),
    acknowledged_at TIMESTAMPTZ,
    resolved_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_severity_created ON alerts(severity, created_at DESC);
CREATE INDEX idx_alerts_unacked ON alerts(is_acknowledged, created_at DESC) WHERE NOT is_acknowledged;
```

### Table: `machine_states`
Current and historical PLC machine operational states.

```sql
CREATE TABLE machine_states (
    id              BIGSERIAL PRIMARY KEY,
    machine_id      VARCHAR(100) NOT NULL,
    machine_name    VARCHAR(200),
    zone_id         VARCHAR(50),
    status          VARCHAR(50) NOT NULL CHECK (status IN ('NOMINAL','WARNING','LOCKED_OUT','MAINTENANCE')),
    operator_id     UUID REFERENCES workers(id),
    reason          TEXT,
    latency_ms      NUMERIC(8,2),   -- Override command execution time
    timestamp       TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_machine_states_machine_time ON machine_states(machine_id, timestamp DESC);
```

### Table: `incidents`
Resolved incident reports generated from alert chains.

```sql
CREATE TABLE incidents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_type   VARCHAR(100) NOT NULL,
    severity        VARCHAR(20) NOT NULL,
    zone_id         VARCHAR(50),
    workers_affected INTEGER DEFAULT 0,
    alert_ids       UUID[] NOT NULL,    -- References to alerts table
    root_cause      TEXT,
    llm_analysis    TEXT,               -- Gemini LLM root cause analysis (v1.3+)
    resolution      TEXT,
    osha_reportable BOOLEAN DEFAULT FALSE,
    started_at      TIMESTAMPTZ NOT NULL,
    resolved_at     TIMESTAMPTZ,
    created_by      UUID REFERENCES workers(id)
);
```

### Table: `sites`
Multi-site federation support (v3.0+).

```sql
CREATE TABLE sites (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_code       VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    location        VARCHAR(500),
    timezone        VARCHAR(100) DEFAULT 'UTC',
    is_active       BOOLEAN DEFAULT TRUE,
    fog_node_ip     INET,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Redis Cache Structure

Redis is used as a **high-speed telemetry cache** with short TTLs.

| Key Pattern | Type | TTL | Contents |
|---|---|---|---|
| `telemetry:snapshot:latest` | JSON string | 30s | Full multi-sensor snapshot |
| `alert:{id}` | JSON string | 3600s | Single alert by ID |
| `alerts:active:list` | List | 60s | Active alert IDs |
| `worker:{id}:vitals` | JSON string | 10s | Latest vitals for one worker |
| `risk:grid:zone-{x}` | JSON string | 250ms | Risk field grid cell |
| `machine:{id}:status` | JSON string | 5s | Current machine state |
| `ws:connections` | Set | — | Active WebSocket connection IDs |

### Cache Write Strategy

```
Fog Node ingest → FastAPI MQTT subscriber
  → asyncio.gather(
      postgres_async_write(reading),    # Async, durable
      redis_cache_set(key, data, ttl)  # Fast, volatile
  )
  → websocket_broadcast(alert_payload)  # Real-time push
```

---

## Migrations

Database migrations are managed by **Alembic**:

```bash
# Initialize migrations (first time only)
alembic init alembic

# Create new migration
alembic revision --autogenerate -m "add fatigue_coefficient to worker_vitals"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

---

## Performance Tuning

Key PostgreSQL configuration for high-throughput sensor ingestion:

```sql
-- postgresql.conf recommendations for Sentinel-X
shared_buffers = 4GB           -- 25% of RAM
effective_cache_size = 12GB    -- 75% of RAM
work_mem = 256MB               -- Per query
max_parallel_workers = 8       -- Match CPU cores
wal_buffers = 64MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1         -- SSD storage assumed
```

Partition pruning is critical — always include `timestamp` in `WHERE` clauses for `sensor_readings` and `worker_vitals`.
