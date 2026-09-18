# Sentinel-X ESP32-S3 Sensor Node Firmware

**Target Hardware:** Espressif ESP32-S3-WROOM-1 (Dual-core Xtensa LX7 @ 240MHz, 512KB SRAM, 8MB Flash)  
**Framework:** ESP-IDF v5.2+ / FreeRTOS  
**Language:** C++17  

---

## 1. Core Architectural Responsibilities

The ESP32-S3 firmware executes the first tier of the Sentinel-X disaster intelligence pipeline:
1. **Periodic Multi-Sensor Sampling (1.0 Hz):** Reads physical/emulated river stage gauge (radar/ultrasonic), barometric pressure (BMP388), soil moisture (TDR), and battery voltage.
2. **Local Kinematic Validation:** Computes kinematic rate-of-rise ($\Delta h / \Delta t$) and tests hydrodynamic physical plausibility bounds.
3. **Autonomous Local Edge Safety:**
   > **PRINCIPLE: RASPBERRY PI FAILURE $\neq$ SAFETY FAILURE.**  
   If water elevation exceeds emergency critical thresholds ($> 3.50\text{m}$) or rate-of-rise breaches warning limits ($> 0.06\text{m/min}$), the node **autonomously actuates a physical 105 dB acoustic siren relay via GPIO 18**, completely independent of gateway availability.
4. **Compact Dual Serialization:** Formats readings into human-readable JSON (for UART console diagnostics) and 24-byte compact binary frames with CRC-16-CCITT (for HF Packet Radio / Satellite / LoRa backhaul).
5. **Hardware Watchdog:** Integrated task watchdog (10-second timeout) with automated core panics and warm restart recovery.

---

## 2. Directory Structure

```
firmware/sensor_node/
├── CMakeLists.txt              # Root build configuration
├── sdkconfig.defaults          # ESP32-S3 target configurations
├── README.md                   # Technical reference & build guide
└── main/
    ├── CMakeLists.txt          # Component manifest
    ├── main.cpp                # FreeRTOS task orchestration & entrypoint
    ├── sensor_manager.h/.cpp   # Normalized sensor driver & plausibility checker
    ├── safety_controller.h/.cpp# Autonomous physical siren & safety decision logic
    ├── telemetry.h/.cpp        # JSON & Compact Binary serialization with CRC16
    ├── node_identity.h/.cpp    # Hardware eFuse Root-of-Trust & signature abstraction
    └── fault_manager.h/.cpp    # Task watchdog & sensor fault isolation
```

---

## 3. How to Build & Flash

### Prerequisites
- ESP-IDF v5.2 or higher installed:
  ```bash
  . $HOME/esp/esp-idf/export.sh
  ```

### Build & Flash Commands
```bash
# 1. Set target to ESP32-S3
idf.py set-target esp32s3

# 2. Build firmware binary
idf.py build

# 3. Flash to connected hardware & open monitor
idf.py -p /dev/ttyUSB0 flash monitor
```

### Desktop Emulation Mode (for Host Testing)
The firmware source code has dual-target compile guards (`#if defined(ESP_PLATFORM)`). It can be compiled directly on Linux/macOS/Windows using `g++`:
```bash
g++ -std=c++17 main/main.cpp main/sensor_manager.cpp main/safety_controller.cpp main/telemetry.cpp main/node_identity.cpp main/fault_manager.cpp -I main -o sensor_node_sim
./sensor_node_sim
```
