# Sentinel-X Data Flow Documentation

## Overview

This document describes the complete data pipeline — from raw IoT sensor measurements through AI processing to the operator cockpit dashboard.

---

## End-to-End Data Flow

```
╔══════════════╗    ╔══════════════╗    ╔══════════════╗    ╔══════════════╗
║  SENSOR DATA ║ ─► ║  FOG INGEST  ║ ─► ║  AI PIPELINE ║ ─► ║   OUTPUTS   ║
╚══════════════╝    ╚══════════════╝    ╚══════════════╝    ╚══════════════╝
```

---

## Stage 1 — Sensor Data Origination

### Worker Biometric Data
```
Smart Helmet (BLE 5.2)
  ├── Heart rate sensor        → HR (bpm) @ 1Hz
  ├── SpO2 pulse oximeter      → SpO2 (%) @ 1Hz
  └── Accelerometer/IMU        → Fall detection @ 50Hz

UWB Positioning System (DW3000)
  ├── 4 UWB anchors per zone
  ├── TDOA triangulation algorithm
  └── 3D position (x,y,z) @ 10Hz, accuracy ±15cm
```

### Environmental Sensor Data
```
Gas Detection Array
  ├── CO2 sensor (NDIR)        → ppm @ 0.5Hz
  ├── H2S sensor (electrochemical) → ppm @ 0.5Hz
  └── LEL combustible gas      → % LEL @ 1Hz

LoRaWAN Environmental Node
  ├── Temperature/Humidity     → °C, % RH @ 0.1Hz
  └── Barometric pressure      → hPa @ 0.1Hz

Vibration Accelerometer (Modbus RTU)
  ├── Bearing vibration        → Hz (FFT) @ 10Hz
  └── Shaft imbalance score    → 0-100 @ 1Hz
```

### Vision Data
```
IP Camera (RTSP)
  ├── Resolution: 3840×2160 (4K)
  ├── Frame rate: 30fps
  └── Encoding: H.264 CBR, 8Mbps
```

---

## Stage 2 — Edge Gateway Ingestion

All sensor data from Stage 1 aggregates at the **Ruggedized IoT Gateway**:

```
IoT Gateway Processing
  ├── MQTT publish (QoS 1) → topic: sentinel/telemetry/{zone}/{sensor_id}
  ├── Data validation & range checking
  ├── Timestamp normalization (UTC)
  ├── Packet buffering (64 reading FIFO per sensor)
  └── Forwarding to Fog Node MQTT broker @ 1883/tcp
```

**MQTT Topic Structure:**
```
sentinel/
  telemetry/
    zone-a/co2/sensor-024          ← Gas readings
    zone-b/temperature/env-007     ← Environmental
    worker/uwb/helmet-w1-john-doe  ← Worker position
    machine/vibration/comp-b       ← Machine vitals
  alerts/
    critical/zone-b/intrusion-001  ← Critical alerts
    warning/zone-a/gas-level-002   ← Warning alerts
  commands/
    machine/lockout/plc-comp-b     ← Outbound PLC commands
```

---

## Stage 3 — Fog Layer AI Processing

```
┌─────────────────────────────────────────────────┐
│ MQTT Subscriber (sentinel/telemetry/#)           │
│   → Telemetry Parser                            │
│   → In-memory ring buffer (last 300 readings)   │
└────────────────────────┬────────────────────────┘
                         │
          ┌──────────────┼──────────────────┐
          │              │                  │
          ▼              ▼                  ▼
   ┌─────────────┐ ┌─────────────┐ ┌───────────────┐
   │ Vision Agent│ │Prediction AI│ │  Route Agent  │
   │             │ │             │ │               │
   │ YOLOv11-TRT │ │ Risk Field  │ │ A* Pathfinder │
   │ 32ms/frame  │ │ Model v3.4  │ │ 15ms/compute  │
   │             │ │ 250ms/grid  │ │               │
   │ Detections: │ │ Output:     │ │ Output:       │
   │ - PPE state │ │ - Risk grid │ │ - Evac routes │
   │ - Zone pos  │ │ - Zone risk │ │ - Exit ETAs   │
   │ - Fall det  │ │ - Forecast  │ │               │
   └──────┬──────┘ └──────┬──────┘ └───────┬───────┘
          │               │                │
          └───────────────▼────────────────┘
                          │
              ┌───────────▼────────────┐
              │  Emergency Response    │
              │       Agent           │
              │                       │
              │  If consensus ≥ 3/4:  │
              │  → Modbus/TCP lockout │
              │  → MQTT alert publish │
              │  → WebSocket push     │
              └───────────────────────┘
```

### Digital DNA Fatigue Coefficient Calculation

```python
# Computed every 30 seconds per worker
fatigue_coefficient = weighted_avg(
    heart_rate_variability_score,   # weight: 0.35
    spo2_deficit_score,             # weight: 0.25
    time_on_floor_score,            # weight: 0.20
    movement_irregularity_score,    # weight: 0.15
    historical_incident_score,      # weight: 0.05
)
# Result: 0.0 (alert) → 1.0 (critically fatigued)
# Threshold alert: > 0.70
```

---

## Stage 4 — Cloud Persistence

```
Fog Node ──HTTPS/TLS──► FastAPI Backend
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
         PostgreSQL          Redis         WebSocket
         (long-term)       (real-time)    (live push)
              │               │                │
         Incident logs   Sensor snapshot   Cockpit UI
         Worker DNA      (30s TTL)         Update
         Audit trails    Risk grid state
```

### Write Path (Alert Event)
```
1. Fog publishes MQTT alert → sentinel/alerts/critical/zone-b/intrusion
2. Backend MQTT subscriber receives message
3. Alert written to PostgreSQL alerts table (async)
4. Alert cached in Redis (key: alert:{id}, TTL 3600s)
5. Alert broadcast to all WebSocket connections (/ws/alerts)
6. Cockpit dashboard receives push, renders alert card
```

### Read Path (Telemetry Query)
```
1. Cockpit UI polls GET /api/v1/sensors/telemetry
2. FastAPI checks Redis key: telemetry:snapshot:latest
3a. Cache HIT  → Return Redis value (< 1ms)
3b. Cache MISS → Query PostgreSQL latest readings
4. Response serialized to JSON
5. Redis cache updated (TTL reset to 30s)
```

---

## Stage 5 — Cockpit Dashboard Rendering

```
FastAPI WebSocket ──push──► Browser WebSocket Client
                                      │
                       ┌──────────────▼──────────────┐
                       │        Tab Router           │
                       │                             │
              ┌────────┴────────┐   ┌────────────────┴──────┐
              │ Alert Stream    │   │  3D Digital Twin       │
              │ addAlert()      │   │  updateWorkerPos()     │
              │ playAlertSound()│   │  renderRiskField()     │
              └─────────────────┘   └───────────────────────┘
```

---

## Data Latency Budget

| Segment | Target | Achieved |
|---|---|---|
| Sensor → Gateway | < 10ms | ~5ms |
| Gateway → Fog MQTT | < 20ms | ~12ms |
| Vision inference (YOLOv11) | < 45ms | 32ms |
| Agent consensus | < 15ms | 11ms |
| PLC Modbus command | < 10ms | 8ms |
| **Total edge override** | **< 100ms** | **84ms** |
| Fog → Cloud HTTPS push | < 200ms | ~140ms |
| WebSocket push to UI | < 50ms | ~18ms |
| **Total to dashboard** | **< 500ms** | **~310ms** |

---

## Data Volume Estimates (Per Site, 100 Workers)

| Data Type | Rate | Daily Volume |
|---|---|---|
| Sensor readings | 1,200 msg/s | ~100M readings/day |
| Video frames | 4 cams × 30fps | ~10M frames/day |
| Position updates | 100 workers × 10Hz | 86M positions/day |
| Alert events | ~50/day average | 50 records/day |
| Audit logs | ~1,000/day | 1,000 records/day |

**PostgreSQL partition strategy:** Time-based monthly partitions on `sensor_readings`, with automated archival to cold storage after 90 days.
