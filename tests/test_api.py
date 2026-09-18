"""
Sentinel-X Comprehensive Test Suite — Disaster Resilience Subsystems
====================================================================
Tests:
  1. Root Metadata & Health Check
  2. System Status & Architecture Endpoint
  3. Disaster Fusion Engine & Risk Calculation
  4. Sensor Trust & Byzantine Quarantine Engine
  5. Telemetry Ingestion & Local SQLite Persistence
  6. Communication Manager 4-Mode Failover
  7. HF Packet Radio (7.105 MHz AX.25) Frame Serialization & CRC
  8. Satellite IoT Compact Burst Framing
  9. Offline Store-and-Forward SQLite Durability & Batch Sync
 10. Post-Quantum Cryptography (ML-KEM / ML-DSA) Session Interfaces
 11. Simulation Scenario Injections (5 SIH Hero Moments)
"""

import pytest
import sys
import os

# Ensure project root and backend are on sys.path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend_dir = os.path.join(_project_root, "backend")
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi.testclient import TestClient
from app.main import app
from app.services.sensor_trust_engine import sensor_trust_engine
from app.services.disaster_fusion_engine import disaster_fusion_engine
from app.services.communication_manager import communication_manager
from app.services.adapters.hf_packet_adapter import hf_packet_adapter
from app.services.adapters.satellite_adapter import satellite_adapter
from app.services.store_and_forward import store_and_forward_service
from app.services.pqc_crypto import pqc_crypto_service

client = TestClient(app)

# ---------------------------------------------------------------------------
# 1. System Health & Metadata
# ---------------------------------------------------------------------------

def test_root_metadata():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Sentinel-X" in data["service"]
    assert data["status"] == "operational"
    assert "disaster_risk" in data["endpoints"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["edge_node"] == "RPI5-EDGE-01"

def test_system_status():
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "ESP32-S3" in data["architecture"]
    assert data["sensor_nodes_count"] == 20

# ---------------------------------------------------------------------------
# 2. Disaster Fusion & Risk Calculation
# ---------------------------------------------------------------------------

def test_disaster_risk_endpoint():
    response = client.get("/api/v1/disasters/current")
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "confidence" in data
    assert "contributing_factors" in data
    assert data["confidence"] >= 80

def test_disaster_fusion_engine_unit():
    # Normal stream
    normal_readings = [{"stage_m": 2.41, "rate_m_min": 0.01} for _ in range(5)]
    normal_risk = disaster_fusion_engine.evaluate_risk(normal_readings)
    assert normal_risk.severity == "NORMAL"
    assert normal_risk.risk_score < 45

    # Critical surge stream
    critical_readings = [{"stage_m": 3.85, "rate_m_min": 0.08} for _ in range(5)]
    critical_risk = disaster_fusion_engine.evaluate_risk(critical_readings)
    assert critical_risk.severity == "CRITICAL"
    assert critical_risk.risk_score >= 75
    assert critical_risk.contributing_factors.water >= 30

# ---------------------------------------------------------------------------
# 3. Sensor Trust & Byzantine Quarantine Engine
# ---------------------------------------------------------------------------

def test_sensor_trust_normal():
    # Normal reading agreeing with neighbors
    trust_res = sensor_trust_engine.evaluate_node("NODE-01", 2.41, 0.01, [2.40, 2.42])
    assert trust_res.status == "VERIFIED"
    assert trust_res.trust_score >= 90.0
    assert len(trust_res.reasons) == 0

def test_sensor_trust_spoof_and_quarantine():
    # Erratic reading: 8.90m when neighbors report 2.41m
    trust_res = sensor_trust_engine.evaluate_node("NODE-03", 8.90, 2.45, [2.41, 2.42])
    assert trust_res.status == "QUARANTINED"
    assert trust_res.trust_score < 50.0
    assert len(trust_res.reasons) >= 1
    assert sensor_trust_engine.is_quarantined("NODE-03")

def test_sensor_trust_matrix_endpoint():
    response = client.get("/api/v1/sensors/trust")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 20

# ---------------------------------------------------------------------------
# 4. Telemetry Ingestion & SQLite Durability
# ---------------------------------------------------------------------------

def test_telemetry_ingestion_api():
    payload = {
        "node_id": "NODE-01",
        "sequence_num": 101,
        "timestamp_ms": 1725720000000,
        "water_level_m": 2.41,
        "rate_of_rise_m_min": 0.01,
        "battery_pct": 95,
        "safety_state": 0,
        "confidence": 0.98
    }
    response = client.post("/api/v1/telemetry/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PROCESSED"
    assert data["node_id"] == "NODE-01"

# ---------------------------------------------------------------------------
# 5. Communication Resilience & Failover State Machine
# ---------------------------------------------------------------------------

def test_comms_status_and_mode_switching():
    # Set to Degraded (HF Packet)
    response = client.post("/api/v1/communications/set-mode/DEGRADED")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "DEGRADED"
    assert data["hf_status"] == "ACTIVE"
    assert data["internet_status"] == "FAILED"

    # Reset to Normal
    response = client.post("/api/v1/communications/set-mode/NORMAL")
    assert response.status_code == 200
    assert response.json()["mode"] == "NORMAL"

def test_hf_packet_radio_ax25_encoding():
    event_payload = {
        "event_id": "EVT-9821",
        "stage_m": 3.85,
        "risk_score": 84,
        "severity": "CRITICAL"
    }
    tx_result = hf_packet_adapter.transmit_emergency_bulletin(event_payload)
    assert tx_result["channel"] == "HF_PACKET_RADIO"
    assert tx_result["frequency_mhz"] == 7.105
    assert len(tx_result["raw_frame_hex"]) > 0
    assert tx_result["status"] == "TRANSMITTED"

def test_satellite_adapter_sbd_framing():
    event_payload = {
        "stage_m": 3.85,
        "rate_m_min": 0.08,
        "risk_score": 84,
        "confidence": 94,
        "battery_pct": 92
    }
    sat_res = satellite_adapter.transmit_burst(event_payload)
    assert sat_res["channel"] == "SATELLITE_IOT"
    assert sat_res["bytes_used"] == 16 # 16 bytes fixed SBD frame
    assert sat_res["status"] == "SENT"


# ---------------------------------------------------------------------------
# 6. Offline Store-and-Forward & Batch Synchronization
# ---------------------------------------------------------------------------

def test_store_and_forward_lifecycle():
    # 1. Clear any prior events
    store_and_forward_service.clear_all()
    assert len(store_and_forward_service.get_pending_events()) == 0

    # 2. Queue an event
    evt_id = store_and_forward_service.queue_event(
        node_id="NODE-02",
        event_type="SURGE_ALERT",
        severity="CRITICAL",
        risk_score=84,
        confidence=94,
        payload={"stage_m": 3.85}
    )
    assert evt_id.startswith("EVT-")
    pending = store_and_forward_service.get_pending_events()
    assert len(pending) == 1
    assert pending[0]["event_id"] == evt_id

    # 3. Batch Sync
    sync_res = store_and_forward_service.sync_all_pending()
    assert sync_res["status"] == "SYNC_COMPLETE"
    assert sync_res["synced_count"] == 1
    assert len(store_and_forward_service.get_pending_events()) == 0

# ---------------------------------------------------------------------------
# 7. Post-Quantum Cryptography Interfaces
# ---------------------------------------------------------------------------

def test_pqc_session_interfaces():
    kem_res = pqc_crypto_service.establish_session_kem()
    assert kem_res["algorithm"] == "ML-KEM-768"
    assert kem_res["ciphertext_len_bytes"] == 1088
    assert kem_res["status"] == "SESSION_ESTABLISHED"

    sig_res = pqc_crypto_service.sign_telemetry_dsa(b"SX_EMERGENCY_FRAME_01")
    assert sig_res["algorithm"] == "ML-DSA-65"
    assert len(sig_res["signature_hex"]) == 64
    assert sig_res["status"] == "VERIFIED"

# ---------------------------------------------------------------------------
# 8. SIH Demonstration Scenarios
# ---------------------------------------------------------------------------

def test_sih_hero_scenarios():
    # Hero 1
    r1 = client.post("/api/v1/simulation/inject", json={"scenario": "disaster_detection"})
    assert r1.status_code == 200
    assert "HERO 1" in r1.json()["result"]

    # Hero 2
    r2 = client.post("/api/v1/simulation/inject", json={"scenario": "sensor_spoofing"})
    assert r2.status_code == 200
    assert "HERO 2" in r2.json()["result"]

    # Hero 3
    r3 = client.post("/api/v1/simulation/inject", json={"scenario": "internet_failure"})
    assert r3.status_code == 200
    assert "HERO 3" in r3.json()["result"]

    # Hero 4
    r4 = client.post("/api/v1/simulation/inject", json={"scenario": "complete_network_loss"})
    assert r4.status_code == 200
    assert "HERO 4" in r4.json()["result"]

    # Hero 5
    r5 = client.post("/api/v1/simulation/inject", json={"scenario": "restoration"})
    assert r5.status_code == 200
    assert "HERO 5" in r5.json()["result"]

    # Reset
    r6 = client.post("/api/v1/simulation/inject", json={"scenario": "reset_normal"})
    assert r6.status_code == 200
    assert "RESET" in r6.json()["result"]
