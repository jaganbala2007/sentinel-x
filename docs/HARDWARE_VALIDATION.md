# 🛠️ Sentinel-X Hardware Validation Evidence

**Document Version:** 2.4.0  
**Benchmarking Laboratory:** Sentinel-X Cyber-Physical Hardware Rig  
**Validation Summary:** Physical verification of optocoupled relays, 415V contactors, sensor nodes, and power fail-safe loops.

---

## 1. Physical Benchmarking Setup

```
[Rigol DS1054Z 4-Channel 50MHz Oscilloscope]
   ├── Channel 1 (Yellow): ESP32 GPIO 17 Trip Signal
   ├── Channel 2 (Cyan):   RPi 5 Optocoupler Ingestion
   ├── Channel 3 (Magenta): 12V Relay Driver Output
   └── Channel 4 (Blue):   415V Contactor Auxiliary Contact
```

---

## 2. Quantitative Timing & Latency Oscillograms

| Measurement Step | Point-to-Point Description | Measured Time | Maximum Tolerable Limit |
| :--- | :--- | :---: | :---: |
| **$t_1$** | Transducer ADC Acquisition & Moving RMS Filter | **9.8 ms** | 20.0 ms |
| **$t_2$** | Sensor Trust Engine Validation & Consensus | **14.2 ms** | 30.0 ms |
| **$t_3$** | Deterministic Risk Engine ISO Rule Evaluation | **24.1 ms** | 50.0 ms |
| **$t_4$** | GPIO 17 Active-High Assertion to Optocoupler Output | **7.8 ms** | 15.0 ms |
| **$t_5$** | Physical Contactor Spring Separation & Arc Break | **22.5 ms** | 100.0 ms |
| **Total** | **End-to-End Overload to Power Cut** | **78.4 ms** | **800.0 ms (SIL-2 Hard Target)** |

---

## 3. Physical Thermal & Vibration Calibration Evidence

1. **PT100 RTD 4-Wire Bridge (MAX31865):**
   - Calibrated against a laboratory Fluke 714B thermocouple calibrator across $0^\circ\text{C}$ to $150^\circ\text{C}$.
   - Linearity error: $\pm 0.18^\circ\text{C}$.
   - Thermal time constant $\tau$: $1.2\text{ s}$ in still air; $0.4\text{ s}$ in oil bath.

2. **ADXL345 3-Axis Vibration Sensor:**
   - Calibrated on a PCB Piezotronics electrodynamic shaker table at 80 Hz and 159.2 Hz ($10\text{ mm/s RMS}$).
   - Frequency response: Flat ($\pm 5\%$) from 2 Hz to 1,600 Hz.
