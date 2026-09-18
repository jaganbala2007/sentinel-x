# SENTINEL-X REST & WEBSOCKET API SPECIFICATION

## Port Configuration
- **Host:** `0.0.0.0`
- **Port:** `8000`
- **Interactive Swagger Docs:** `http://<PI_IP>:8000/docs`

---

## 1. Core Endpoints

### `GET /`
Returns the landing page file or the current authoritative digital twin state.

### `GET /api/health`
Health diagnostic endpoint returning status of SQLite, MQTT, and edge processing.
```json
{
  "status": "healthy",
  "service": "Sentinel-X Edge Engine",
  "systemMode": "LIVE",
  "mqtt": "CONNECTED",
  "edge_node": "RPI3-EDGE-01",
  "storage": "SQLite WAL Buffer Active",
  "timestamp": 1789606800
}
```

### `GET /api/v1/twin/state` (Primary Authoritative Endpoint)
Combines physical sensor states, derived risk scores, Byzantine trust metrics, explainable safety decisions, and incident logs into one single source of truth.
```json
{
  "system": "Sentinel-X",
  "systemStatus": "ONLINE",
  "digitalTwin": "ACTIVE",
  "node1": {
    "nodeId": "NODE-01",
    "pir": 0,
    "gas": 420,
    "temperature": 32.9,
    "humidity": 82.8,
    "trustScore": 100,
    "riskLevel": "NORMAL",
    "status": "ONLINE",
    "lastPacketAgo": 0.5,
    "hazards": [],
    "anomalies": []
  },
  "node2": {
    "nodeId": "NODE-02",
    "gas": 374,
    "temperature": 32.7,
    "humidity": 80.2,
    "current": -0.48,
    "vibration": 2.16,
    "sound": 336,
    "trustScore": 100,
    "riskLevel": "NORMAL",
    "status": "ONLINE",
    "lastPacketAgo": 0.8,
    "hazards": [],
    "anomalies": []
  },
  "riskScore": 0,
  "riskLevel": "NORMAL",
  "safetyDecision": "SAFE",
  "safetyDetail": {
    "why": "All environmental and machine parameters operating within baseline safety limits.",
    "evidence": ["Node-01 gas & thermal nominal", "Node-02 vibration 2.16 below trigger"],
    "action": "Maintain routine industrial monitoring",
    "confidence": 98
  },
  "isInterlocked": false,
  "alarmActive": false,
  "commState": "NORMAL",
  "activeChannel": "INTERNET",
  "mqtt": "CONNECTED",
  "powerState": "NORMAL"
}
```

---

## 2. Ingestion & Actuation Endpoints

### `POST /api/v1/telemetry`
HTTP fallback ingestion for sensor packets.
- Body: Node 01 or Node 02 JSON payload.

### `POST /api/v1/safety/interlock`
Triggers immediate safety interlock, setting system state to ISOLATE, risk to CRITICAL, and activating alarms.

### `POST /api/v1/system/recover`
Recovers system from interlock/hazard states to nominal baseline.

---

## 3. Simulation & Fault Endpoints (Demo Mode)

### `POST /api/v1/fault/spoof`
Simulates gas sensor spoof/spike (gas raw ADC = 2650).

### `POST /api/v1/fault/comms`
Simulates LAN/Internet failure, shifting communication to blackbox edge mode.

### `POST /api/v1/fault/power`
Simulates primary grid loss, shifting system to battery buffer.

### `POST /api/v1/fault/hazard`
Simulates machine thermal and vibration anomaly (vibration = 8.4, temp = 94.5°C).

---

## 4. WebSocket Telemetry

### `WS /ws/telemetry`
Real-time streaming socket pushing authoritative state at 1 Hz with zero-overhead JSON frames.
Fallback to HTTP `GET /api/v1/twin/state` polling is automatically handled by the frontend.
