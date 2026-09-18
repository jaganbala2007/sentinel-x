# Sentinel-X V2 — Sensor Abstraction & Adapter Architecture

## 1. Universal Hardware-in-the-Loop Normalization

A core architectural principle of Sentinel-X V2 is:
> **The Core Intelligence, Trust Engine, and Risk Engine never communicate directly with vendor-specific physical sensor registers.**

All hardware interfaces feed polymorphic sensor adapters that output an identical, standardized **`NormalizedSensorReading`** data contract:

```
[Physical Hardware]                      [Simulation Engine]
  • JSN-SR04T (GPIO Pulse)                 • Synthetic Hydrology (Teesta)
  • BMP280 / SHT40 (I2C)                   • Thermal / Fire Model
  • MQ-4 / MQ-7 (ADC / SPI)                • Gas Plume Model
  • Modbus RTU / 4-20mA                    • Resonant Vibration Model
         │                                          │
         ▼                                          ▼
 [Hardware Adapter]                         [Simulation Adapter]
         │                                          │
         └────────────────────┬─────────────────────┘
                              ▼
                 NormalizedSensorReading:
                 {
                   node_id: "NODE-01",
                   timestamp_ms: 1725720000000,
                   sensor_type: "ultrasonic_depth",
                   metric_name: "water_level_m",
                   value: 2.45,
                   unit: "m",
                   location: { lat, lon, bldg, floor, zone },
                   battery_pct: 95,
                   hardware_health: "HEALTHY",
                   confidence: 0.98
                 }
                              │
                              ▼
            Sentinel-X Core Processing Pipeline
```

---

## 2. Sensor Driver Adapter Catalog

### 1. I2C / SPI Adapter (`I2CSensorAdapter`)
- **Protocol:** Hardware I2C on ESP32-S3 (SDA: GPIO 21, SCL: GPIO 22) operating at 100 kHz / 400 kHz bus clock.
- **Supported Sensors:**
  - `BMP280` / `BME280`: Atmospheric pressure, temperature, relative humidity.
  - `SHT40`: High-precision thermal / humidity monitoring.
  - `MPU6050` / `ADXL345`: Triaxial tilt and structural acceleration.

### 2. GPIO Pulse / Ultrasonic Adapter (`PulseTimingAdapter`)
- **Protocol:** Microsecond hardware timer input capture.
- **Supported Sensors:**
  - `JSN-SR04T` / `HC-SR04`: Waterproof ultrasonic distance measurement.
  - Trigger pulse: 10 µs high pulse on GPIO 5; Echo pulse measured via hardware edge timer on GPIO 19.

### 3. Analog / ADC Adapter with OSR Calibration (`AnalogSensorAdapter`)
- **Protocol:** ESP32-S3 12-bit SAR ADC with 64x hardware oversampling (OSR) and linear voltage reference calibration.
- **Supported Sensors:**
  - Gas Sensors (`MQ-2`, `MQ-4`, `MQ-7`): Toxic/combustible gas concentration.
  - Soil Moisture Transducer.
  - Battery DC Bus Voltage Divider (100kΩ / 20kΩ scaling down 12.6V to 2.1V).

### 4. Industrial RS-485 / Modbus Adapter (`ModbusRTUAdapter`)
- **Protocol:** Differential RS-485 via MAX485 / ISO3082 transceiver over UART2 (TX: GPIO 17, RX: GPIO 16, DE/RE: GPIO 4).
- **Supported Peripherals:**
  - Industrial 4-20mA current-loop transmitters.
  - Modbus RTU PLC telemetry registers.
  - Pipeline overpressure transducers.

---

## 3. Compact Binary Serialization Protocol

For bandwidth-constrained links (HF Packet Radio at 300–1200 baud, Satellite SBD at 340 bytes/packet), Sentinel-X serializes readings into an ultra-dense **24-byte binary telemetry frame**:

| Byte Offset | Field Name | Data Type | Encoding / Units |
| :---: | :--- | :---: | :--- |
| `0` | Protocol Sync Word | `uint8` | `0x53` ('S') |
| `1` | Protocol Version | `uint8` | `0x02` (v2.0) |
| `2..3` | Node ID Identifier | `uint16` | Hash of Node Call-sign |
| `4..7` | Sequence Number | `uint32` | Monotonically increasing |
| `8..11` | Timestamp Offset | `uint32` | Unix epoch seconds |
| `12..13` | Metric Value | `int16` | Fixed-point ($0.01\times$ value) |
| `14..15` | Auxiliary Metric | `int16` | Fixed-point ($0.01\times$ value) |
| `16` | Battery Level | `uint8` | Percentage $0\dots 100\%$ |
| `17` | Safety State Flags | `uint8` | Bit 0: Siren, Bit 1: Quarantined |
| `18` | Environment Type | `uint8` | Enum $0\dots 5$ |
| `19..21` | Reserved | `3 bytes` | Forward compatibility |
| `22..23` | CRC-16 Checksum | `uint16` | CRC-16-CCITT ($x^{16} + x^{12} + x^5 + 1$) |

**Total Frame Size:** Exactly **24 bytes**. Transmittable over HF radio in under **160 milliseconds** at 1200 baud.
