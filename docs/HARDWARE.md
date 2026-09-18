# Sentinel-X Hardware Architecture & BOM Guide

**Hardware Classification:** Defense-Grade Ruggedized IoT Disaster Sensing Fleet  
**Status:** HARDWARE-READY SPECIFICATION & COMPILABLE FIRMWARE  

---

## 1. Subsystem Hardware Overview

```
                      +-----------------------------+
                      |   SOLAR ARRAY (200W)        |
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      | MPPT CHARGE CONTROLLER (20A)|
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      | LiFePO4 BATTERY (24V, 50Ah) |
                      +--------------+--------------+
                                     |
               +---------------------+---------------------+
               |                                           |
+--------------v---------------+            +--------------v--------------+
| RASPBERRY PI 5 GATEWAY (8GB) |            | ESP32-S3 SENSOR NODES (x20) |
| - Broadcom BCM2712 Quad A76  |            | - Dual Xtensa LX7 @ 240MHz  |
| - 64GB eMMC Flash (WAL)      |            | - 512KB SRAM, 8MB Flash     |
| - HF TNC Modem Interface     |            | - Hardware eFuse Secure Boot|
| - LEO Satellite Transceiver  |            | - Optical Radar Stage Sensor|
+--------------+---------------+            | - BMP388 Barometric Pressure|
               |                            | - TDR Soil Moisture Probe   |
+--------------v---------------+            | - 105 dB Acoustic Siren Relay|
| HF TRANSCEIVER (40m / 7MHz)  |            +-----------------------------+
| - Yaesu FT-891 / QRP SDR     |
| - NVIS Dipole Antenna        |
+------------------------------+
```

---

## 2. Sensor Node Bill of Materials (Per Node)

| Component | Part Number | Interface | Purpose | Approx. Cost (INR) |
| :--- | :--- | :--- | :--- | :--- |
| **Microcontroller** | Espressif ESP32-S3-WROOM-1 | SPI/UART/I2C/ADC | Primary processing & FreeRTOS | ₹450 |
| **River Stage Sensor**| 80GHz Millimeter-Wave Radar | RS-485 Modbus / UART | Non-contact water level (0.01m res) | ₹3,200 |
| **Barometric Pressure**| Bosch Sensortec BMP388 | I2C | High-precision pressure & altimetry | ₹480 |
| **Soil Moisture** | TDR Time-Domain Reflectometer| Analog ADC / 4-20mA | Catchment saturation percentage | ₹850 |
| **Local Siren Relay**| Optocoupled 10A Solid-State | GPIO 18 Active-High | Autonomous hardware siren tripping | ₹120 |
| **Power Cell** | LiFePO4 32650 (3.2V, 6000mAh)| Battery ADC Divider | Autonomous local backup power | ₹650 |
| **Enclosure** | IP67 Die-Cast Aluminum | N/A | Weatherproof flood immersion | ₹750 |
| **Total Per Node** | | | | **₹6,500** |

---

## 3. Edge Gateway Bill of Materials

| Component | Specification | Purpose |
| :--- | :--- | :--- |
| **Gateway Host** | Raspberry Pi 5 (8GB RAM, Active Cooler) | Local edge intelligence & database persistence |
| **Storage** | 64GB Industrial Grade eMMC (Class 10) | SQLite Write-Ahead-Logging local event buffer |
| **HF Packet Radio TNC**| Direwolf Audio Modem / NinoTNC | 1200 Baud AFSK AX.25 packet modulation |
| **HF Transceiver**| 20W NVIS QRP Transceiver (7.105 MHz) | Emergency ionospheric disaster transmission |
| **Power Bank** | 24V 50Ah LiFePO4 with 20A MPPT Solar | 72-Hour continuous off-grid runtime |
