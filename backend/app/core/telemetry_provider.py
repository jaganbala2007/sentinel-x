"""
Sentinel-X Telemetry Provider & Digital Twin Simulation Engine
==============================================================
Provides a unified normalized telemetry architecture supporting:
  1. ONLINE Mode: Live physical ESP32 sensor nodes (Node 1, Node 2) via MQTT / Raspberry Pi 4.
  2. OFFLINE Mode: Realistic Digital Twin Simulation Engine with temporal continuity,
     physics-constrained temperature/humidity coupling, MQ-135 raw ADC modeling,
     and ADXL345 3-axis vibration dynamics.

Both modes feed the exact same downstream Alert Engine, Validation Engine,
Database, and WebSocket streams.
"""

import time
import math
import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Normalized Telemetry Schema
# ---------------------------------------------------------------------------

class NodeTelemetry(BaseModel):
    node_id: str = Field(..., description="ESP32 hardware ID e.g. SX-NODE-01")
    zone: str = Field(..., description="Plant Zone e.g. ZONE-1 or ZONE-2")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    data_source: str = Field(..., description="'LIVE' or 'SIMULATION'")
    status: str = Field("ONLINE", description="'ONLINE', 'OFFLINE', or 'DEGRADED'")
    last_received: Optional[str] = None

    # Environmental Sensors (DHT22)
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative Humidity in percentage")

    # Air Quality Sensor (MQ-135)
    mq135_raw: int = Field(..., description="Raw ADC reading (0-4095)")
    air_quality_status: str = Field("GOOD", description="'GOOD', 'MODERATE', 'POOR', 'CRITICAL'")

    # Vibration & Acceleration (ADXL345)
    accel_x: float = Field(0.0, description="X-axis acceleration in m/s^2")
    accel_y: float = Field(0.0, description="Y-axis acceleration in m/s^2")
    accel_z: float = Field(9.81, description="Z-axis acceleration in m/s^2 (includes gravity)")
    accel_magnitude: float = Field(9.81, description="Vector magnitude sqrt(x^2 + y^2 + z^2)")
    vibration_status: str = Field("NORMAL", description="'NORMAL', 'ELEVATED', 'HIGH', 'CRITICAL'")
    vibration_hz: float = Field(2.1, description="Dominant vibration frequency in Hz")


class SystemTelemetrySnapshot(BaseModel):
    timestamp: str
    mode: str = Field(..., description="'ONLINE' or 'OFFLINE'")
    data_source_label: str = Field(..., description="'LIVE SENSOR DATA' or 'DIGITAL TWIN SIMULATION'")
    nodes: Dict[str, NodeTelemetry]
    alerts_active: List[Dict[str, Any]]
    system_status: str = Field("SYSTEM HEALTHY", description="Overall plant health summary")


# ---------------------------------------------------------------------------
# Digital Twin Simulation Engine
# ---------------------------------------------------------------------------

class SimulationScenario:
    NORMAL = "Normal Operation"
    HIGH_TEMP = "High Temperature"
    AIR_QUALITY = "Air Quality Deterioration"
    VIBRATION_ANOMALY = "Vibration Anomaly"
    MULTI_SENSOR = "Multi-Sensor Safety Event"
    CUSTOM = "Custom Scenario"


class DigitalTwinSimulationEngine:
    """
    Physically-constrained industrial time-series generator.
    Generates realistic drift, Gaussian noise, thermodynamic temperature-humidity
    cross-coupling, and smooth scenario progressions.
    """

    def __init__(self, seed: int = 20260828):
        self.seed = seed
        self.rng = random.Random(seed)
        self.running = True
        self.paused = False
        self.speed = 1.0  # 0.5x, 1x, 2x, 5x, 10x
        self.duration = 60.0  # seconds
        self.scenario = SimulationScenario.NORMAL
        self.elapsed_sim_time = 0.0
        self.last_tick = time.time()

        # Zone 1 Baselines (Assembly Bay)
        self.z1_temp_base = 28.5
        self.z1_temp = 28.5
        self.z1_hum_base = 58.0
        self.z1_hum = 58.0
        self.z1_mq135_base = 1840
        self.z1_mq135 = 1840
        self.z1_vib_base = 1.8
        self.z1_vib = 1.8

        # Zone 2 Baselines (Compressor Bay M-007)
        self.z2_temp_base = 31.0
        self.z2_temp = 31.0
        self.z2_hum_base = 52.0
        self.z2_hum = 52.0
        self.z2_mq135_base = 1910
        self.z2_mq135 = 1910
        self.z2_vib_base = 2.4
        self.z2_vib = 2.4

    def reset(self, new_seed: Optional[int] = None):
        if new_seed is not None:
            self.seed = new_seed
        self.rng = random.Random(self.seed)
        self.elapsed_sim_time = 0.0
        self.last_tick = time.time()
        self.z1_temp = self.z1_temp_base
        self.z1_hum = self.z1_hum_base
        self.z1_mq135 = self.z1_mq135_base
        self.z1_vib = self.z1_vib_base

        self.z2_temp = self.z2_temp_base
        self.z2_hum = self.z2_hum_base
        self.z2_mq135 = self.z2_mq135_base
        self.z2_vib = self.z2_vib_base

    def set_scenario(self, scenario_name: str, duration: float = 60.0):
        self.scenario = scenario_name
        self.duration = max(10.0, float(duration))
        self.elapsed_sim_time = 0.0

    def set_speed(self, speed: float):
        self.speed = max(0.1, min(20.0, float(speed)))

    def tick(self, dt: float = 1.0) -> Dict[str, NodeTelemetry]:
        """
        Advances simulation physics by dt * speed seconds.
        """
        if self.paused or not self.running:
            # Maintain current telemetry state
            return self._build_telemetry()

        step_dt = dt * self.speed
        self.elapsed_sim_time += step_dt
        t = self.elapsed_sim_time

        # Calculate Scenario Intensity (0.0 to 1.0 curve with bell-shaped event progression)
        # Progresses from 0 -> 1.0 (peak at 60% duration) then returns to normal
        if self.duration > 0:
            norm_t = min(1.0, t / self.duration)
            if norm_t < 0.6:
                intensity = norm_t / 0.6
            else:
                intensity = max(0.0, 1.0 - (norm_t - 0.6) / 0.4)
        else:
            intensity = 0.0

        # -------------------------------------------------------------
        # Physical Ambient Drift + Gaussian Noise
        # -------------------------------------------------------------
        # Slow 10-minute sinusoidal ambient cycle
        drift_sin = math.sin(t * 0.01) * 0.4

        # Zone 1 Calculations (Assembly Bay)
        noise_t1 = self.rng.gauss(0, 0.04)
        noise_h1 = self.rng.gauss(0, 0.12)
        noise_g1 = self.rng.gauss(0, 3.0)
        noise_v1 = self.rng.gauss(0, 0.05)

        # Zone 2 Calculations (High-Pressure Compressor M-007)
        noise_t2 = self.rng.gauss(0, 0.06)
        noise_h2 = self.rng.gauss(0, 0.15)
        noise_g2 = self.rng.gauss(0, 4.5)
        noise_v2 = self.rng.gauss(0, 0.08)

        # Scenario Injections
        z1_temp_event = 0.0
        z1_gas_event = 0.0
        z1_vib_event = 0.0

        z2_temp_event = 0.0
        z2_gas_event = 0.0
        z2_vib_event = 0.0

        if self.scenario == SimulationScenario.HIGH_TEMP:
            # Zone 1 Heating Event up to +14°C
            z1_temp_event = intensity * 14.2

        elif self.scenario == SimulationScenario.AIR_QUALITY:
            # Zone 1/2 Gas Leak Event (MQ-135 climbs from 1840 -> 3400)
            z1_gas_event = intensity * 1150
            z2_gas_event = intensity * 1550

        elif self.scenario == SimulationScenario.VIBRATION_ANOMALY:
            # Zone 2 Compressor Bearing Failure (vibration climbs from 2.4 -> 8.6 mm/s)
            z2_vib_event = intensity * 6.4

        elif self.scenario == SimulationScenario.MULTI_SENSOR:
            # Zone 2 Complex Safety Cascade (Temp + Gas + Vibration)
            z2_temp_event = intensity * 12.8
            z2_gas_event = intensity * 1350
            z2_vib_event = intensity * 5.9

        # Continuous Exponential Smoothing / Temporal Filter for Realism (alpha = 0.15)
        alpha = min(1.0, 0.15 * step_dt)

        target_z1_temp = self.z1_temp_base + drift_sin + noise_t1 + z1_temp_event
        self.z1_temp += alpha * (target_z1_temp - self.z1_temp)

        # Thermodynamic coupling: As temperature rises, relative humidity decreases
        temp_hum_coupling_1 = (self.z1_temp - self.z1_temp_base) * 0.8
        target_z1_hum = self.z1_hum_base - temp_hum_coupling_1 + noise_h1
        self.z1_hum += alpha * (target_z1_hum - self.z1_hum)

        target_z1_mq = self.z1_mq135_base + noise_g1 + z1_gas_event
        self.z1_mq135 += alpha * (target_z1_mq - self.z1_mq135)

        target_z1_vib = self.z1_vib_base + noise_v1 + z1_vib_event
        self.z1_vib += alpha * (target_z1_vib - self.z1_vib)

        # Zone 2
        target_z2_temp = self.z2_temp_base + drift_sin * 1.1 + noise_t2 + z2_temp_event
        self.z2_temp += alpha * (target_z2_temp - self.z2_temp)

        temp_hum_coupling_2 = (self.z2_temp - self.z2_temp_base) * 0.9
        target_z2_hum = self.z2_hum_base - temp_hum_coupling_2 + noise_h2
        self.z2_hum += alpha * (target_z2_hum - self.z2_hum)

        target_z2_mq = self.z2_mq135_base + noise_g2 + z2_gas_event
        self.z2_mq135 += alpha * (target_z2_mq - self.z2_mq135)

        target_z2_vib = self.z2_vib_base + noise_v2 + z2_vib_event
        self.z2_vib += alpha * (target_z2_vib - self.z2_vib)

        return self._build_telemetry()

    def _classify_air_quality(self, raw_adc: int) -> str:
        if raw_adc < 2000:
            return "GOOD"
        elif raw_adc < 2500:
            return "MODERATE"
        elif raw_adc < 3100:
            return "POOR"
        return "CRITICAL"

    def _classify_vibration(self, vib_val: float) -> str:
        if vib_val < 3.2:
            return "NORMAL"
        elif vib_val < 4.8:
            return "ELEVATED"
        elif vib_val < 6.8:
            return "HIGH"
        return "CRITICAL"

    def _build_telemetry(self) -> Dict[str, NodeTelemetry]:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Generate ADXL345 3-axis physics
        # Normal gravity on Z: ~9.81 m/s^2, small dynamic oscillation based on vibration
        z1_ax = self.rng.gauss(0, 0.08)
        z1_ay = self.rng.gauss(0, 0.08)
        z1_az = 9.81 + (self.z1_vib * 0.2) + self.rng.gauss(0, 0.1)
        z1_mag = math.sqrt(z1_ax**2 + z1_ay**2 + z1_az**2)

        z2_ax = self.rng.gauss(0, 0.12) * (self.z2_vib / 2.0)
        z2_ay = self.rng.gauss(0, 0.12) * (self.z2_vib / 2.0)
        z2_az = 9.81 + (self.z2_vib * 0.35) + self.rng.gauss(0, 0.15)
        z2_mag = math.sqrt(z2_ax**2 + z2_ay**2 + z2_az**2)

        node1 = NodeTelemetry(
            node_id="SX-NODE-01",
            zone="ZONE-1",
            timestamp=now_iso,
            data_source="SIMULATION",
            status="ONLINE",
            last_received=now_iso,
            temperature=round(self.z1_temp, 1),
            humidity=round(max(10.0, min(99.0, self.z1_hum)), 1),
            mq135_raw=int(round(self.z1_mq135)),
            air_quality_status=self._classify_air_quality(int(round(self.z1_mq135))),
            accel_x=round(z1_ax, 2),
            accel_y=round(z1_ay, 2),
            accel_z=round(z1_az, 2),
            accel_magnitude=round(z1_mag, 2),
            vibration_status=self._classify_vibration(self.z1_vib),
            vibration_hz=round(self.z1_vib, 1),
        )

        node2 = NodeTelemetry(
            node_id="SX-NODE-02",
            zone="ZONE-2",
            timestamp=now_iso,
            data_source="SIMULATION",
            status="ONLINE",
            last_received=now_iso,
            temperature=round(self.z2_temp, 1),
            humidity=round(max(10.0, min(99.0, self.z2_hum)), 1),
            mq135_raw=int(round(self.z2_mq135)),
            air_quality_status=self._classify_air_quality(int(round(self.z2_mq135))),
            accel_x=round(z2_ax, 2),
            accel_y=round(z2_ay, 2),
            accel_z=round(z2_az, 2),
            accel_magnitude=round(z2_mag, 2),
            vibration_status=self._classify_vibration(self.z2_vib),
            vibration_hz=round(self.z2_vib, 1),
        )

        return {
            "SX-NODE-01": node1,
            "SX-NODE-02": node2,
        }


# ---------------------------------------------------------------------------
# Global Telemetry Provider Manager
# ---------------------------------------------------------------------------

class TelemetryModeManager:
    """
    Manages active operational mode:
      - 'ONLINE': Live Physical ESP32 Hardware
      - 'OFFLINE': Digital Twin Simulation Engine
    """

    def __init__(self):
        self.mode = "OFFLINE"  # Default to OFFLINE Digital Twin Simulation on launch
        self.simulation_engine = DigitalTwinSimulationEngine(seed=20260828)
        self.live_nodes: Dict[str, NodeTelemetry] = {}
        self.live_node_last_seen: Dict[str, float] = {}
        self.node_timeout_sec = 15.0  # 15s before flagging node offline in LIVE mode
        self.history_buffer: List[Dict[str, Any]] = []
        self.max_history = 500

    def set_mode(self, new_mode: str) -> Dict[str, Any]:
        valid_modes = ["ONLINE", "OFFLINE"]
        mode_upper = new_mode.strip().upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid mode '{new_mode}'. Must be 'ONLINE' or 'OFFLINE'.")

        old_mode = self.mode
        self.mode = mode_upper

        if self.mode == "OFFLINE":
            self.simulation_engine.reset()
            self.simulation_engine.running = True
            self.simulation_engine.paused = False

        return {
            "previous_mode": old_mode,
            "current_mode": self.mode,
            "data_source_label": "LIVE SENSOR DATA" if self.mode == "ONLINE" else "DIGITAL TWIN SIMULATION",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def ingest_live_reading(self, payload: Dict[str, Any]) -> NodeTelemetry:
        """
        Ingests real physical telemetry from ESP32 Node 1 or Node 2 via MQTT / REST.
        """
        node_id = payload.get("node_id", "SX-NODE-01")
        zone = payload.get("zone", "ZONE-1")
        now_iso = datetime.now(timezone.utc).isoformat()

        # Calculate ADXL345 vector magnitude if provided
        ax = float(payload.get("accel_x", 0.0))
        ay = float(payload.get("accel_y", 0.0))
        az = float(payload.get("accel_z", 9.81))
        mag = math.sqrt(ax**2 + ay**2 + az**2)

        raw_mq = int(payload.get("mq135_raw", 1850))
        vib_hz = float(payload.get("vibration_hz", 2.1))

        telemetry = NodeTelemetry(
            node_id=node_id,
            zone=zone,
            timestamp=now_iso,
            data_source="LIVE",
            status="ONLINE",
            last_received=now_iso,
            temperature=float(payload.get("temperature", 28.0)),
            humidity=float(payload.get("humidity", 55.0)),
            mq135_raw=raw_mq,
            air_quality_status=self.simulation_engine._classify_air_quality(raw_mq),
            accel_x=ax,
            accel_y=ay,
            accel_z=az,
            accel_magnitude=round(mag, 2),
            vibration_status=self.simulation_engine._classify_vibration(vib_hz),
            vibration_hz=vib_hz
        )

        self.live_nodes[node_id] = telemetry
        self.live_node_last_seen[node_id] = time.time()
        self._record_history(telemetry)
        return telemetry

    def get_current_snapshot(self) -> SystemTelemetrySnapshot:
        now_iso = datetime.now(timezone.utc).isoformat()

        if self.mode == "ONLINE":
            nodes_dict = {}
            current_time = time.time()

            # Ensure SX-NODE-01 and SX-NODE-02 are represented
            for n_id, default_zone in [("SX-NODE-01", "ZONE-1"), ("SX-NODE-02", "ZONE-2")]:
                if n_id in self.live_nodes:
                    node = self.live_nodes[n_id]
                    last_seen = self.live_node_last_seen.get(n_id, 0)
                    if current_time - last_seen > self.node_timeout_sec:
                        # Flag Node as OFFLINE without substituting fake data
                        node.status = "OFFLINE"
                    nodes_dict[n_id] = node
                else:
                    # Node never connected in live mode
                    nodes_dict[n_id] = NodeTelemetry(
                        node_id=n_id,
                        zone=default_zone,
                        timestamp=now_iso,
                        data_source="LIVE",
                        status="OFFLINE",
                        last_received=None,
                        temperature=0.0,
                        humidity=0.0,
                        mq135_raw=0,
                        air_quality_status="UNKNOWN",
                        accel_x=0.0,
                        accel_y=0.0,
                        accel_z=0.0,
                        accel_magnitude=0.0,
                        vibration_status="OFFLINE",
                        vibration_hz=0.0
                    )

            label = "LIVE SENSOR DATA"
        else:
            # OFFLINE Digital Twin Simulation
            nodes_dict = self.simulation_engine.tick()
            label = "DIGITAL TWIN SIMULATION"
            for node in nodes_dict.values():
                self._record_history(node)

        # Evaluate Active Alerts
        alerts = self._evaluate_safety_alerts(nodes_dict)

        status_text = "SYSTEM HEALTHY"
        if any(a.get("severity") == "CRITICAL" for a in alerts):
            status_text = "CRITICAL HAZARD DETECTED"
        elif any(a.get("severity") == "WARNING" for a in alerts):
            status_text = "WARNING: SENSORS ELEVATED"

        return SystemTelemetrySnapshot(
            timestamp=now_iso,
            mode=self.mode,
            data_source_label=label,
            nodes=nodes_dict,
            alerts_active=alerts,
            system_status=status_text
        )

    def _evaluate_safety_alerts(self, nodes: Dict[str, NodeTelemetry]) -> List[Dict[str, Any]]:
        alerts = []
        for n_id, n in nodes.items():
            if n.status == "OFFLINE":
                if self.mode == "ONLINE":
                    alerts.append({
                        "node_id": n_id,
                        "zone": n.zone,
                        "title": f"{n.zone} NODE OFFLINE",
                        "description": f"Physical sensor node {n_id} is disconnected. Last seen: {n.last_received or 'Never'}",
                        "severity": "WARNING",
                        "code": "ERR_NODE_DISCONNECTED",
                        "timestamp": n.timestamp
                    })
                continue

            # Temperature Check (> 33°C is warning, > 38°C is critical)
            if n.temperature > 38.0:
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} HIGH TEMPERATURE ALARM",
                    "description": f"Surface temperature reached {n.temperature}°C (Limit: 38.0°C)",
                    "severity": "CRITICAL",
                    "code": "ALERT_TEMP_CRITICAL",
                    "timestamp": n.timestamp
                })
            elif n.temperature > 33.0:
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} ELEVATED TEMPERATURE",
                    "description": f"Ambient temperature elevated to {n.temperature}°C",
                    "severity": "WARNING",
                    "code": "ALERT_TEMP_WARNING",
                    "timestamp": n.timestamp
                })

            # Air Quality Check (MQ-135 > 2500)
            if n.mq135_raw >= 3100:
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} AIR QUALITY CRITICAL",
                    "description": f"MQ-135 raw sensor index at {n.mq135_raw} ADC. Evacuate zone.",
                    "severity": "CRITICAL",
                    "code": "ALERT_GAS_CRITICAL",
                    "timestamp": n.timestamp
                })
            elif n.mq135_raw >= 2500:
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} AIR QUALITY DETERIORATION",
                    "description": f"MQ-135 raw sensor index elevated ({n.mq135_raw} ADC)",
                    "severity": "WARNING",
                    "code": "ALERT_GAS_WARNING",
                    "timestamp": n.timestamp
                })

            # Vibration Check
            if n.vibration_status == "CRITICAL":
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} MACHINE VIBRATION CRITICAL",
                    "description": f"ADXL345 sensor detected severe bearing vibration ({n.vibration_hz} Hz)",
                    "severity": "CRITICAL",
                    "code": "ALERT_VIB_CRITICAL",
                    "timestamp": n.timestamp
                })
            elif n.vibration_status in ["ELEVATED", "HIGH"]:
                alerts.append({
                    "node_id": n_id,
                    "zone": n.zone,
                    "title": f"{n.zone} VIBRATION ANOMALY",
                    "description": f"Machine shaft vibration increased to {n.vibration_hz} Hz",
                    "severity": "WARNING",
                    "code": "ALERT_VIB_WARNING",
                    "timestamp": n.timestamp
                })

        return alerts

    def _record_history(self, telemetry: NodeTelemetry):
        entry = telemetry.dict()
        self.history_buffer.append(entry)
        if len(self.history_buffer) > self.max_history:
            self.history_buffer.pop(0)

    def get_history(self, node_id: Optional[str] = None, data_source: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = self.history_buffer
        if node_id:
            results = [r for r in results if r.get("node_id") == node_id]
        if data_source:
            results = [r for r in results if r.get("data_source") == data_source]
        return results[-limit:]


# Global singleton instance
telemetry_manager = TelemetryModeManager()
