# Sentinel-X Firmware

Edge device firmware for the Smart Safety Helmet and IoT sensor nodes.

## Overview

The firmware runs on two target platforms:

| Platform | MCU | RTOS | Language |
|---|---|---|---|
| Smart Safety Helmet | Nordic nRF5340 | Zephyr RTOS 3.6 | C / C++ |
| Ruggedized IoT Gateway | NXP i.MX 8M Plus | Linux (Yocto) | C++ / Python |

---

## Smart Helmet Firmware (`helmet/`)

### Features
- **BLE 5.2** advertisement and connection management
- **UWB DW3000** TDOA ranging protocol for indoor positioning (±15cm)
- **MAX30102** optical heart rate and SpO2 sensing (1Hz)
- **LSM6DSO** 6-axis IMU with fall detection algorithm (< 50ms response)
- **Battery Management** — LiPo charge monitoring with 16h target life
- **ESTOP Button** — Hardware panic button to trigger SOS broadcast
- **Zephyr BLE Mesh** — Worker-to-worker proximity collision alerting

### Zephyr Application Structure

```
firmware/helmet/
├── src/
│   ├── main.c                  # Application entry point
│   ├── ble/
│   │   ├── ble_service.c       # Custom GATT service definitions
│   │   └── ble_mesh.c          # BLE mesh peer-to-peer
│   ├── sensors/
│   │   ├── heart_rate.c        # MAX30102 driver interface
│   │   ├── spo2.c              # SpO2 dual-wavelength computation
│   │   ├── imu.c               # LSM6DSO 6-axis driver
│   │   └── fall_detect.c       # Threshold + ML fall algorithm
│   ├── uwb/
│   │   ├── uwb_ranging.c       # DW3000 TDOA ranging
│   │   └── uwb_position.c      # 3D position computation
│   └── power/
│       └── battery.c           # LiPo monitoring + sleep management
├── include/
│   └── sentinel_types.h        # Common structs and constants
├── CMakeLists.txt
├── prj.conf                    # Zephyr project config
├── boards/
│   └── nrf5340dk.overlay       # Board-specific pin mapping
└── Kconfig                     # Feature selection
```

### Build Instructions

```bash
# Prerequisites: Zephyr SDK 0.16.x, nRF Connect SDK 2.6.x

# Initialize Zephyr workspace
west init -m https://github.com/nrfconnect/sdk-nrf --mr v2.6.0
west update

# Build for nRF5340 DK
cd firmware/helmet
west build -b nrf5340dk_nrf5340_cpuapp

# Flash
west flash

# Serial monitor (115200 baud)
west espressif monitor
```

### BLE Advertising Payload

```
AD Type: 0xFF (Manufacturer Specific)
Manufacturer ID: 0xFFFF (placeholder)
Payload (12 bytes):
  [0]     Worker ID (1 byte, 0x01–0xFF)
  [1]     Heart rate (1 byte, bpm)
  [2]     SpO2 (1 byte, %)
  [3]     Fatigue score (1 byte, 0–255 mapped to 0.0–1.0)
  [4–5]   Battery level (2 bytes, mV)
  [6]     Status flags:
           Bit 0: PPE helmet worn
           Bit 1: Fall detected
           Bit 2: SOS active
           Bit 3: Low battery
  [7–11]  Reserved
```

---

## IoT Gateway Firmware (`gateway/`)

### Features
- MQTT broker client (Paho C++) with QoS 1 persistence
- 4-20mA ADC sampling (gas sensors) via industrial DAQ board
- Serial Modbus RTU to vibration sensors
- LoRaWAN packet forwarder (Semtech legacy protocol)
- Local ring-buffer (64 readings/sensor) for network resilience
- Watchdog and automatic recovery on crash

### Gateway Software Stack

```
gateway/
├── src/
│   ├── main.cpp                # Application entry
│   ├── mqtt/
│   │   ├── mqtt_client.cpp     # Paho MQTT publish wrapper
│   │   └── topic_builder.cpp   # sentinel/ topic construction
│   ├── sensors/
│   │   ├── adc_sampler.cpp     # 4-20mA gas sensor ADC
│   │   ├── modbus_reader.cpp   # Vibration sensor Modbus RTU
│   │   └── lora_gateway.cpp    # LoRaWAN packet processor
│   └── storage/
│       └── ring_buffer.cpp     # Local sensor FIFO buffer
├── include/
├── CMakeLists.txt
└── config.yaml                 # Gateway MQTT + sensor configuration
```

---

## Planned Firmware Improvements (v2.1)

- [ ] ATEX Zone 1 rated enclosure integration
- [ ] Secure BLE pairing with certificate-based authentication
- [ ] FOTA (Firmware Over The Air) updates via BLE DFU
- [ ] NFC worker identification tag (ISO 14443)
- [ ] Skin temperature sensor for heat stress detection
- [ ] Machine learning fall detection model (TensorFlow Lite Micro)

---

*For hardware specifications, see [hardware/README.md](../hardware/README.md).*
