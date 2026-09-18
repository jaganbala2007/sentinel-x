"""
Sentinel-X Authoritative Digital Twin State Manager
====================================================
Single source of truth for live hardware (ESP32 Node-01, Node-02),
simulation telemetry, sensor watchdog timers, Byzantine trust verification,
and explainable safety decisions.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.services.disaster_risk_engine import risk_engine
from app.services.multi_sensor_correlation import correlation_engine
from app.services.disaster_state_machine import disaster_state_machine
from app.services.zone_manager import zone_manager
from app.services.evacuation_manager import evacuation_manager
from app.services.post_disaster_engine import post_disaster_engine
from app.services.scenario_engine import scenario_engine

class SentinelTwinStateManager:
    def __init__(self):
        self.system_mode: str = "SIMULATION"  # "LIVE", "SIMULATION", "OFFLINE"
        self.system_status: str = "ONLINE"
        self.digital_twin_status: str = "ACTIVE"
        
        self.mqtt_status: str = "CONNECTED"
        self.comm_state: str = "NORMAL"
        self.active_channel: str = "INTERNET"
        self.power_state: str = "NORMAL"
        
        self.is_interlocked: bool = False
        self.alarm_active: bool = False
        self.camera_status: str = "ONLINE"
        self.ppe_engine_status: str = "ACTIVE"
        self.current_role: str = "DISASTER_COMMANDER"
        
        # Node Watchdogs (seconds)
        self.node_timeout_seconds: float = 5.0
        
        # Node 1 State (Environmental + Worker Safety)
        self.node1: Dict[str, Any] = {
            "nodeId": "NODE-01",
            "pir": 0,
            "gas": 420,
            "temperature": 32.9,
            "humidity": 82.8,
            "trustScore": 100,
            "riskLevel": "NORMAL",
            "status": "ONLINE",
            "lastSeen": time.time(),
            "lastPacketAgo": 0.0,
            "hazards": [],
            "anomalies": []
        }
        
        # Node 2 State (Machine Health)
        self.node2: Dict[str, Any] = {
            "nodeId": "NODE-02",
            "gas": 374,
            "temperature": 32.7,
            "humidity": 80.2,
            "current": -0.66,
            "vibration": 2.16,
            "sound": 336,
            "trustScore": 100,
            "riskLevel": "NORMAL",
            "status": "ONLINE",
            "lastSeen": time.time(),
            "lastPacketAgo": 0.0,
            "hazards": [],
            "anomalies": []
        }
        
        self.risk_score: int = 0
        self.risk_level: str = "NORMAL"
        self.safety_decision: str = "SAFE"
        self.safety_detail: Dict[str, Any] = {
            "why": "All environmental and machine parameters operating within baseline safety limits.",
            "evidence": ["Node-01 gas & thermal nominal", "Node-02 vibration 2.16 mm/s below trigger"],
            "action": "Maintain routine industrial monitoring",
            "confidence": 98,
            "contributors": []
        }
        
        self.incidents: List[Dict[str, Any]] = [
            {
                "id": "INC-8901",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "node": "NODE-02",
                "zone": "ZONE_B",
                "disaster_type": "FIRE_SMOKE_HAZARD",
                "trigger": "BASELINE_VERIFICATION",
                "severity": "INFO",
                "status": "CLOSED",
                "operator": "SYSTEM_AUTONOMOUS",
                "resolution": "Initial edge calibration passed."
            }
        ]
        
        self.audit_log: List[Dict[str, Any]] = [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "SYSTEM",
                "event": "SENTINEL_EDGE_INITIALIZED",
                "severity": "INFO",
                "prevState": "STARTUP",
                "newState": "ONLINE",
                "reason": "Raspberry Pi 4 Edge Brain service online."
            }
        ]
        
        self.fault_flags: Dict[str, bool] = {
            "spoof": False,
            "comms": False,
            "power": False,
            "hazard": False
        }

    def update_node1(self, data: Dict[str, Any]):
        now = time.time()
        self.node1["lastSeen"] = now
        self.node1["status"] = "ONLINE"
        
        if "pir" in data: self.node1["pir"] = int(data["pir"])
        if "gas" in data: self.node1["gas"] = int(data["gas"])
        if "temperature" in data: self.node1["temperature"] = float(data["temperature"])
        if "humidity" in data: self.node1["humidity"] = float(data["humidity"])
        
        self._evaluate_safety_state()

    def update_node2(self, data: Dict[str, Any]):
        now = time.time()
        self.node2["lastSeen"] = now
        self.node2["status"] = "ONLINE"
        
        if "gas" in data: self.node2["gas"] = int(data["gas"])
        if "temperature" in data: self.node2["temperature"] = float(data["temperature"])
        if "humidity" in data: self.node2["humidity"] = float(data["humidity"])
        if "current" in data: self.node2["current"] = float(data["current"])
        if "vibration" in data: self.node2["vibration"] = float(data["vibration"])
        if "sound" in data: self.node2["sound"] = int(data["sound"])
        
        self._evaluate_safety_state()

    def check_watchdogs(self):
        now = time.time()
        n1_ago = now - self.node1["lastSeen"]
        n2_ago = now - self.node2["lastSeen"]
        
        self.node1["lastPacketAgo"] = round(n1_ago, 1)
        self.node2["lastPacketAgo"] = round(n2_ago, 1)
        
        if self.system_mode == "LIVE":
            if n1_ago > self.node_timeout_seconds:
                self.node1["status"] = "OFFLINE"
                self.node1["trustScore"] = max(10, self.node1["trustScore"] - 20)
            else:
                self.node1["status"] = "ONLINE"
                
            if n2_ago > self.node_timeout_seconds:
                self.node2["status"] = "OFFLINE"
                self.node2["trustScore"] = max(10, self.node2["trustScore"] - 20)
            else:
                self.node2["status"] = "ONLINE"

    def _evaluate_safety_state(self):
        self.check_watchdogs()

        # Run Multi-Sensor Correlation Engine
        corr_res = correlation_engine.evaluate_telemetry(self.node1, self.node2, self.camera_status)
        
        # Run Explainable Risk Calculation Engine
        combined_telemetry = {**self.node1, "vibration": self.node2["vibration"]}
        risk_res = risk_engine.calculate_risk(combined_telemetry)

        self.risk_score = risk_res["risk_score"]
        self.risk_level = risk_res["risk_level"]

        if self.risk_level == "CRITICAL":
            self.safety_decision = "ISOLATE"
            self.alarm_active = True
            self.is_interlocked = True
            zone_manager.update_zone_status("ZONE_B", "CRITICAL", 3, "EVACUATE")
            evacuation_manager.trigger_evacuation("ZONE_B")
            if disaster_state_machine.current_state not in ["CRITICAL", "RESPONSE", "STABILIZATION", "RECOVERY"]:
                disaster_state_machine.transition_to("CRITICAL", "Multi-sensor critical breach detected", "SYSTEM_AUTO")
        elif self.risk_level == "WARNING":
            self.safety_decision = "WARN"
            zone_manager.update_zone_status("ZONE_B", "WARNING", 2, "WARNING")
            if disaster_state_machine.current_state in ["NORMAL", "WATCH"]:
                disaster_state_machine.transition_to("WARNING", "Multi-sensor warning threshold reached", "SYSTEM_AUTO")
        else:
            self.safety_decision = "SAFE"
            if disaster_state_machine.current_state in ["WATCH", "WARNING"] and not self.fault_flags["hazard"]:
                disaster_state_machine.transition_to("NORMAL", "Telemetry parameters stabilized", "SYSTEM_AUTO")

        self.safety_detail = {
            "why": f"Correlated Event: {corr_res['event_type']} ({corr_res['severity']})",
            "evidence": corr_res["evidence"],
            "action": corr_res["recommended_action"],
            "confidence": corr_res["confidence"],
            "contributors": risk_res["contributors"],
            "equation": risk_res["equation"]
        }

    def get_authoritative_state(self) -> Dict[str, Any]:
        self.check_watchdogs()
        return {
            "system": "SENTINEL-X",
            "systemTitle": "Edge-AI Disaster Resilience, Situational Awareness & Response System",
            "systemStatus": self.system_status,
            "digitalTwin": self.digital_twin_status,
            "systemMode": self.system_mode,
            "currentRole": self.current_role,
            "disasterLifecycleState": disaster_state_machine.current_state,
            
            "node1": {
                "nodeId": self.node1["nodeId"],
                "pir": self.node1["pir"],
                "gas": self.node1["gas"],
                "temperature": self.node1["temperature"],
                "humidity": self.node1["humidity"],
                "trustScore": self.node1["trustScore"],
                "riskLevel": self.node1["riskLevel"],
                "status": self.node1["status"],
                "lastPacketAgo": self.node1["lastPacketAgo"],
                "hazards": self.node1["hazards"],
                "anomalies": self.node1["anomalies"]
            },
            
            "node2": {
                "nodeId": self.node2["nodeId"],
                "gas": self.node2["gas"],
                "temperature": self.node2["temperature"],
                "humidity": self.node2["humidity"],
                "current": self.node2["current"],
                "vibration": self.node2["vibration"],
                "sound": self.node2["sound"],
                "trustScore": self.node2["trustScore"],
                "riskLevel": self.node2["riskLevel"],
                "status": self.node2["status"],
                "lastPacketAgo": self.node2["lastPacketAgo"],
                "hazards": self.node2["hazards"],
                "anomalies": self.node2["anomalies"]
            },
            
            "riskScore": self.risk_score,
            "riskLevel": self.risk_level,
            "safetyDecision": self.safety_decision,
            "safetyDetail": self.safety_detail,
            "isInterlocked": self.is_interlocked,
            "alarmActive": self.alarm_active,
            "commState": self.comm_state,
            "activeChannel": self.active_channel,
            "mqtt": self.mqtt_status,
            "powerState": self.power_state,
            "camera": self.camera_status,
            "ppeEngine": self.ppe_engine_status,
            "zones": zone_manager.get_all_zones()["zones"],
            "evacuation": evacuation_manager.get_evacuation_state(),
            "lifecycle": disaster_state_machine.get_status(),
            "incidents": self.incidents,
            "auditLog": self.audit_log[-10:]
        }


    def inject_fault(self, fault_type: str) -> Dict[str, Any]:
        fault_type = fault_type.lower()
        if fault_type == "spoof":
            self.fault_flags["spoof"] = True
            self.node1["gas"] = 2650
        elif fault_type == "comms":
            self.comm_state = "DEGRADED"
            self.active_channel = "HF_RADIO"
        elif fault_type == "power":
            self.power_state = "BATTERY"
        elif fault_type == "hazard":
            self.fault_flags["hazard"] = True
            self.node2["temperature"] = 94.5
            self.node2["vibration"] = 8.4
        self._evaluate_safety_state()
        return self.get_authoritative_state()

    def recover(self) -> Dict[str, Any]:
        self.fault_flags = {"spoof": False, "comms": False, "power": False, "hazard": False}
        self.is_interlocked = False
        self.alarm_active = False
        self.comm_state = "NORMAL"
        self.active_channel = "INTERNET"
        self.power_state = "NORMAL"
        self.node1["gas"] = 420
        self.node1["temperature"] = 32.9
        self.node2["vibration"] = 2.16
        self.node2["temperature"] = 32.7
        self._evaluate_safety_state()
        return self.get_authoritative_state()

twin_state_manager = SentinelTwinStateManager()
