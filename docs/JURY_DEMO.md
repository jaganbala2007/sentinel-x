# Sentinel-X Jury Demo Execution Guide

## Presenter Steps

1. **System Startup**:
   - Ensure Mosquitto, Backend, and Dashboard are running (`./status.sh`).
   - Open Command Center: `http://localhost:3000` (or `http://10.242.228.126:3000`).

2. **Scenario Pipeline Demonstration**:
   - **NORMAL**: System displays `SAFE` decision and baseline telemetry.
   - **GAS HAZARD**: Trigger gas leak scenario via Demo Panel or API `POST /api/v1/fault/spoof`. Evidence chain shows MQ135 ADC elevation.
   - **HIGH TEMPERATURE / OVERHEAT**: Trigger `POST /api/v1/fault/hazard`. Node-02 temperature rises to 94.5°C, vibration rises to 8.4 mm/s, emergency E-stop interlock trips, 3D digital twin motor turns red.
   - **COMMUNICATION FAILOVER**: Trigger `POST /api/v1/fault/comms`. System enters `DEGRADED` mode and switches active channel to 7.105 MHz AX.25 HF Packet Radio.
   - **RECOVERY**: Press `[RESET]` or call `POST /api/v1/system/recover` to restore baseline operation.
   - **AUDIT REPORT**: Click `[EXPORT JSON]` or `[EXPORT CSV]` to download certified audit files.
