# SENTINEL-X Hardware Architecture & Wiring Guide
## SIH 2026 Problem Statement ID: 26223

This document details the hardware assembly, pinouts, local MQTT broker configuration, and Raspberry Pi 4 edge controller setup for SENTINEL-X.

---

## 1. System Hardware Block Diagram

```
  ┌────────────────────────────────────────────────────────┐
  │                 FIELD SENSOR NODE (ESP32)              │
  │                                                        │
  │  [ DHT22 ] ─────── GPIO 4  (Temp / Humidity)           │
  │  [ MQ-135 ] ────── ADC1_CH6 (Air Quality / Gas)         │
  │  [ ADXL345 ] ───── I2C (SDA: GPIO 21, SCL: GPIO 22)    │
  │  [ Relay / Siren ] GPIO 26 (Local Interlock Output)    │
  │  [ LED Indicator] GPIO 2  (Status Beacon)              │
  └───────────────────────────┬────────────────────────────┘
                              │
                    WiFi / Local MQTT (1883)
                              │
  ┌───────────────────────────▼────────────────────────────┐
  │              EDGE CONTROLLER (Raspberry Pi 4)          │
  │                                                        │
  │  - Mosquitto MQTT Broker (port 1883)                   │
  │  - USB / CSI Web Camera Feed (port 8080)               │
  │  - Local SQLite WAL Database (sentinel_edge.db)        │
  │  - FastAPI Edge Intelligence & Risk Engine (port 8000)  │
  │  - Offline Store-and-Forward WAL Buffer                 │
  └───────────────────────────┬────────────────────────────┘
                              │
                    Local Ethernet / Wi-Fi
                              │
  ┌───────────────────────────▼────────────────────────────┐
  │            SENTINEL-X COMMAND CENTER (Browser UI)      │
  │  - 3D Three.js Spatial Digital Twin                    │
  │  - Zone Hazard Map (Green / Amber / Orange / Red)      │
  │  - Multi-Sensor Correlation & Explainable Risk Panel   │
  │  - Incident Command & Evacuation Controller            │
  └────────────────────────────────────────────────────────┘
```

---

## 2. ESP32 Sensor Pinout & Connection Mapping

| Sensor Module | Physical Pin / Interface | ESP32 Pin | Voltage | Function |
| :--- | :--- | :--- | :--- | :--- |
| **DHT22** | DATA | GPIO 4 | 3.3V | Temperature & Relative Humidity |
| **MQ-135** | AOUT (Analog Out) | GPIO 34 (ADC1_CH6) | 5.0V | Air Quality & Hazardous Gas ADC |
| **ADXL345** | SDA | GPIO 21 | 3.3V | I2C Data (Kinematic Acceleration) |
| **ADXL345** | SCL | GPIO 22 | 3.3V | I2C Clock (Kinematic Acceleration) |
| **Buzzer / Relay** | IN | GPIO 26 | 5.0V | Local Acoustic Emergency Alarm |
| **Status LED** | ANODE | GPIO 2 | 3.3V | Onboard Diagnostic Pulse |

---

## 3. Raspberry Pi 4 Edge Gateway Setup

### A. Mosquitto MQTT Broker Installation
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

### B. SQLite WAL Buffer Configuration
The edge backend uses SQLite Write-Ahead Logging (WAL) for high concurrency and zero data loss:
```bash
# In backend/app/core/database.py
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
```

### C. Offline Store-and-Forward Operation
1. When internet/cloud connectivity drops, the Raspberry Pi 4 continues local operation uninterrupted.
2. Telemetry, risk scores, operator actions, and alerts are queued in `offline_events` in `sentinel_edge.db`.
3. When network connectivity returns, queued records auto-sync to upstream cloud/central servers.

---

## 4. Camera Feed Integration
Connect a standard USB Webcam or Raspberry Pi Camera module:
```bash
# Install MJPG-Streamer or OpenCV Streamer
mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 1280x720 -f 30" -o "output_http.so -w /usr/local/www -p 8080"
```
The camera stream is embedded into the Sentinel-X Command Center UI for visual incident verification.
