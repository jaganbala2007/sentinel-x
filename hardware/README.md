# Sentinel-X Hardware Guide

## Overview

This document covers the complete hardware bill of materials, wiring diagrams, and integration specifications for the Sentinel-X physical deployment.

---

## Bill of Materials (BoM)

| # | Component | Model | Qty | Unit Cost (USD) | Total |
|---|---|---|---|---|---|
| 1 | Edge AI Compute Node | NVIDIA Jetson Orin NX 16GB | 1 | $499 | $499 |
| 2 | Smart Safety Helmet | Custom BLE 5.2 / UWB DW3000 | 10 | $120 | $1,200 |
| 3 | Gas Detector (CO2/H2S) | Dräger Polytron 8100 | 4 | $200 | $800 |
| 4 | LoRaWAN Environmental Node | Dragino LA66 + SHT20 | 6 | $45 | $270 |
| 5 | LoRaWAN Gateway | Dragino LPS8N | 1 | $130 | $130 |
| 6 | 4K Industrial IP Camera | Hikvision DS-2CD2T47G2 | 4 | $150 | $600 |
| 7 | UWB Anchor (Indoor Positioning) | Decawave DW3000 EVK | 8 | $80 | $640 |
| 8 | Ruggedized IoT Gateway | Moxa UC-8200 | 1 | $350 | $350 |
| 9 | WearOS Smartwatch (Worker) | Custom WearOS 3.x | 10 | $90 | $900 |
| 10 | Industrial PLC | Siemens SIMATIC S7-1200 | 2 | $400 | $800 |
| 11 | Managed PoE Switch | Cisco SG250-26P | 1 | $350 | $350 |
| 12 | Vibration Accelerometer | IMI Sensors 686B01 | 4 | $220 | $880 |
| 13 | Noise Level Meter | PCE-SLT10 IoT | 4 | $120 | $480 |
| 14 | DIN Rail + Enclosure | Fibox PC 403028 IP67 | 2 | $80 | $160 |
| **TOTAL** | | | | | **~$8,059** |

---

## Network Topology

```
Internet / Cloud
      │
      │ HTTPS/TLS
      ▼
  Site VPN Gateway (pfSense)
      │
      ├── LAN A: IT Network (192.168.1.0/24)
      │     ├── Fog Node / Jetson Orin (192.168.1.100)
      │     ├── Nginx Server (192.168.1.101)
      │     └── NTP Server
      │
      ├── LAN B: OT Network - ISOLATED (10.10.0.0/24)
      │     ├── PLC Compressor B (10.10.0.200)
      │     ├── PLC Boiler A (10.10.0.201)
      │     └── Safety Relay Panel (10.10.0.210)
      │
      └── LAN C: IoT/Sensor Network (10.20.0.0/24)
            ├── Ruggedized Gateway (10.20.0.1)
            ├── IP Cameras x4 (10.20.0.10–13)
            └── UWB Anchors x8 (10.20.0.20–27)
```

> **CRITICAL:** The OT Network (PLC) must be physically isolated from the IT network. Only the Fog Node has bridged access via a one-way firewall rule for Modbus/TCP.

---

## Smart Helmet Design

```
┌──────────────────────────────────────┐
│     Custom Smart Safety Helmet       │
│                                      │
│  ┌────────────┐  ┌─────────────────┐ │
│  │  MCU       │  │  UWB DW3000     │ │
│  │  Nordic    │  │  2-Way Ranging  │ │
│  │  nRF5340   │  │  Accuracy ±15cm │ │
│  └─────┬──────┘  └─────────────────┘ │
│        │                              │
│  ┌─────▼──────┐  ┌─────────────────┐ │
│  │ HR + SpO2  │  │  BLE 5.2        │ │
│  │ MAX30102   │  │  → Gateway      │ │
│  └────────────┘  └─────────────────┘ │
│                                      │
│  ┌────────────┐  ┌─────────────────┐ │
│  │ IMU 6-axis │  │  LiPo 2000mAh   │ │
│  │ LSM6DSO    │  │  (16h life)     │ │
│  │ Fall detect│  │  USB-C charge   │ │
│  └────────────┘  └─────────────────┘ │
└──────────────────────────────────────┘
```

### Firmware Features (Zephyr RTOS)
- **Heart Rate:** MAX30102 optical sensor, 1Hz sampling
- **SpO2:** Dual-wavelength (660nm/940nm), ±2% accuracy
- **Fall Detection:** IMU-based threshold algorithm, < 50ms response
- **UWB Ranging:** TDOA with 8 anchors for 3D position
- **BLE Advertising:** Device UUID + encrypted payload to gateway
- **Battery:** 16-hour continuous operation, charging indicator

---

## Jetson Orin NX Configuration

### Hardware Specs
- **CPU:** 8-core Arm Cortex-A78AE
- **GPU:** 1024-core Ampere CUDA
- **Memory:** 16GB LPDDR5
- **Storage:** 256GB NVMe SSD
- **I/O:** 4× USB 3.2, 4× MIPI CSI, Gigabit Ethernet, M.2 PCIe

### Software Stack
- **OS:** JetPack 6.0 (Ubuntu 22.04 LTS)
- **CUDA:** 12.4
- **TensorRT:** 10.0
- **AI Inference:** YOLOv11s (PPE), YOLOv11-pose (fall detection), custom risk field model
- **MQTT Client:** Paho C++ (QoS 1)
- **PLC Interface:** libmodbus v3.1.10
- **Runtime:** Custom C++ Multi-Agent Mesh Engine

---

## PLC Wiring (Modbus/TCP Override)

```
Fog Node (192.168.1.100)
    │
    │ Ethernet — Modbus/TCP (Port 502)
    ▼
Siemens S7-1200 (10.10.0.200)
    │
    ├── Output Q0.0 ──► Compressor B ESTOP relay
    ├── Output Q0.1 ──► Boiler A shutdown valve
    ├── Output Q0.2 ──► Conveyor motor contactor
    └── Output Q0.3 ──► Chemical pump relay

Emergency Override Logic:
  Modbus Write Single Coil (FC5) to Q0.x = 0xFF00 (FORCE ON → ESTOP)
  Executes in < 8ms LAN round-trip
```

---

## Certifications Required for Production

| Certification | Body | Scope |
|---|---|---|
| ATEX Zone 1 (IECEx) | IECEx | Smart Helmet in explosive environments |
| CE Mark | EU | All electronics placed on EU market |
| FCC Part 15 | FCC | BLE/UWB radio emissions (US) |
| IP67 | IEC 60529 | Helmet and sensor enclosures |
| ISO 45001:2018 | ISO | Overall occupational safety management |

---

*For firmware source code, see [firmware/README.md](../firmware/README.md).*
