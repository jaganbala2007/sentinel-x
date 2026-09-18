# Sentinel-X V2 — Universal Environment Profiles Specification

## 1. Overview & Architectural Decoupling

In Sentinel-X V2, the **Core Safety Intelligence Platform** is completely environment-agnostic. All environment-specific sensor configurations, physical bounds, hazard models, communication priorities, and response policies are partitioned into clean, declarative **Environment Profiles**.

```
                           SENTINEL-X CORE PLATFORM
           (Sensor Trust • Bayesian Risk • Edge Autonomy • Comms Failover)
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
[NATURAL_OUTDOOR]              [INDOOR_BUILDING]             [INDUSTRIAL]
 River / Watershed              High-Rise / Campus            Chemical / Plant
 Flash Flood / Surge            Fire / Smoke / Gas            Toxic Gas / Pressure
 JSN-SR04T / BMP280             Optical Smoke / SHT40         Catalytic / Modbus
 GPS / GIS Elevation            Building / Floor / Room       Plant Topological

         ▼                            ▼                            ▼
[CRITICAL_INFRASTRUCTURE]      [REMOTE_DISASTER_ZONE]        [CUSTOM PROFILE]
 Bridge / Dam / Viaduct         Isolated Mountain Basin       User-Configured
 Structural Vibration / Tilt    Off-Grid Flash Flood          Extensible Schema
 Triaxial Accel / Inclinometer  Low-Power Solar / Depth       Dynamic Thresholds
 GNSS / Pier Coordinate         HF Direct Radio Priority      Runtime Swappable
```

---

## 2. Environment Profile Catalog

### Profile 1: `NATURAL_OUTDOOR` (SIH Flagship Hero Profile)
- **Target Environments:** River catchments, dams, mountain gorges, floodplains, reservoirs, coastal zones.
- **Active Hazards:** `FLASH_FLOOD`, `FLOOD`, `LANDSLIDE`, `POWER_FAILURE`.
- **Primary Sensors:**
  - Waterproof Ultrasonic Depth (`JSN-SR04T`): Range $0.0\dots 12.0$ m; Kinematic rate limit $0.40$ m/min.
  - Barometric Pressure (`BMP280`): Range $850.0\dots 1080.0$ hPa; Drop indicates cyclonic storm front.
  - Ambient Temperature / Humidity (`SHT40` / `BME280`): $-10.0\dots 55.0$ °C.
  - Tipping-Bucket Rain Gauge & Soil Moisture Probe.
- **Spatial Reference:** Geographic GIS (WGS84 Latitude/Longitude/Elevation).
- **Communication Priority:** `INTERNET` $\to$ `HF_PACKET` (7.105 MHz AX.25) $\to$ `SATELLITE` $\to$ `OFFLINE`.
- **Autonomous Response Actions:**
  - Local audible/strobe siren actuation on ESP32-S3 GPIO 18 when water $\ge 3.50$ m or rate $\ge 0.08$ m/min.
  - Dispatch evacuation corridor advisories via HF emergency packet radio.

---

### Profile 2: `INDOOR_BUILDING`
- **Target Environments:** Commercial high-rises, institutional campuses, hospitals, data centers, warehouses.
- **Active Hazards:** `FIRE`, `SMOKE`, `GAS_LEAK`, `POWER_FAILURE`.
- **Primary Sensors:**
  - Optical Particle Smoke Obscuration: Range $0.0\dots 20.0$ %/m; Warning threshold $1.5$ %/m; Critical threshold $4.0$ %/m.
  - Ambient Temperature: $5.0\dots 120.0$ °C; Warning threshold $45.0$ °C; Critical threshold $65.0$ °C.
  - Carbon Monoxide (`CO`): $0\dots 1000$ ppm; Critical threshold $50.0$ ppm.
- **Spatial Reference:** Topological Building Coordinates (`Building_ID`, `Floor_Level`, `Room_or_Zone`). *No GPS required indoors.*
- **Communication Priority:** `INTERNET` $\to$ `ETHERNET` $\to$ `WIFI` $\to$ `OFFLINE`.
- **Autonomous Response Actions:**
  - Actuate local building fire alarm & strobe circuit.
  - Signal building management system (BMS) for stairwell pressurization fan start.

---

### Profile 3: `INDUSTRIAL`
- **Target Environments:** Chemical synthesis plants, refineries, manufacturing decks, compressor halls, utility tunnels.
- **Active Hazards:** `GAS_LEAK`, `FIRE`, `EQUIPMENT_FAILURE`, `POWER_FAILURE`.
- **Primary Sensors:**
  - Catalytic Combustible / Toxic Gas (`MQ-4` / `MQ-7` / 4-20mA Industrial Transmitters): Range $0\dots 5000$ ppm; Critical threshold $100.0$ ppm.
  - Piezoelectric Industrial Vibration: $0.0\dots 50.0$ mm/s RMS; Warning $4.5$ mm/s; Critical $7.5$ mm/s.
  - Manifold Line Pressure: $0.0\dots 30.0$ bar; Critical overpressure $22.0$ bar.
- **Spatial Reference:** Topological Plant Zones (`Plant_ID`, `Process_Bay`, `Manifold_Tag`).
- **Communication Priority:** `ETHERNET_MODBUS` $\to$ `INTERNET` $\to$ `HF_PACKET` $\to$ `OFFLINE`.
- **Autonomous Response Actions:**
  - Signal emergency valve isolation relay.
  - Engage industrial exhaust scrubbers.
  - Sound plant evacuation horn.

---

### Profile 4: `CRITICAL_INFRASTRUCTURE`
- **Target Environments:** Highway viaducts, suspension bridges, dam retaining walls, railway tunnels.
- **Active Hazards:** `STRUCTURAL_ANOMALY`, `FLOOD`, `POWER_FAILURE`.
- **Primary Sensors:**
  - Triaxial Low-Noise Accelerometer: Vibration $0.0\dots 40.0$ mm/s; Warning $4.0$ mm/s; Critical $7.5$ mm/s.
  - Digital Dual-Axis Inclinometer: Angular Tilt $-10.0\dots +10.0$°; Critical threshold $2.0$°.
  - Pier Foundation Scour Depth Probe.
- **Spatial Reference:** Structural Span & Pier Coordinate Matrix.
- **Communication Priority:** `INTERNET` $\to$ `SATELLITE` $\to$ `HF_PACKET` $\to$ `OFFLINE`.
- **Autonomous Response Actions:**
  - Actuate highway closure gates and load restriction beacons.
  - Alert Department of Transportation dispatch.

---

### Profile 5: `REMOTE_DISASTER_ZONE`
- **Target Environments:** Isolated valleys and disaster-stricken territories where cellular towers, grid electricity, and roads are destroyed.
- **Active Hazards:** `FLASH_FLOOD`, `LANDSLIDE`, `POWER_FAILURE`.
- **Primary Sensors:**
  - Ultrasonic Runoff Depth Sensor & Solar Bus Voltage Monitor.
  - Ground Geophone / Vibration Sensor.
- **Spatial Reference:** High-altitude mountain terrain coordinates.
- **Communication Priority:** `HF_PACKET` (Primary) $\to$ `SATELLITE` $\to$ `OFFLINE_STORE_AND_FORWARD`.
- **Autonomous Response Actions:**
  - Local siren on-node alert.
  - Buffer all emergency frames into SQLite; broadcast via 40-meter HF ionospheric ground/skywave.

---

## 3. Dynamic Profile Switching API

Environment profiles can be switched on-the-fly via the REST API or Dashboard Switcher without restarting the edge services:

```http
POST /api/v1/environment/switch
Content-Type: application/json

{
  "profile_id": "INDUSTRIAL"
}
```

```json
{
  "status": "success",
  "message": "Active environment profile switched to Industrial Chemical & Process Facility",
  "profile": {
    "id": "INDUSTRIAL",
    "name": "Industrial Chemical & Process Facility",
    "active_hazards": ["GAS_LEAK", "FIRE", "EQUIPMENT_FAILURE", "POWER_FAILURE"]
  },
  "assessment": {
    "overall_risk_score": 15,
    "overall_severity": "NORMAL",
    "primary_threat": "GAS_LEAK"
  }
}
```
