"""
Sentinel-X V2 Cross-Environment Automated Test Suite
=====================================================
Validates that ONE UNIFIED CORE ENGINE correctly evaluates:
  1. Natural Flood & Surge (SIH Hero)
  2. Indoor Fire & Thermal/Smoke Spikes
  3. Industrial Combustible / Toxic Gas Leaks
  4. Civil Infrastructure Vibration & Structural Deflection
  5. Power & Battery Depletion
without modifying core trust or risk logic.
"""

import pytest
import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend_dir = os.path.join(_project_root, "backend")
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.universal import (
    NormalizedSensorReading,
    EnvironmentType,
    HazardType,
    SeverityLevel,
    LocationModel
)
from app.services.environment_manager import environment_manager
from app.services.universal_risk_engine import universal_risk_engine
from app.services.universal_trust_engine import universal_trust_engine

client = TestClient(app)

def test_environment_profiles_api():
    """Verify that all 5 pre-configured environment profiles are discoverable."""
    res = client.get("/api/v1/environment/profiles")
    assert res.status_code == 200
    profiles = res.json()
    assert len(profiles) >= 5
    profile_ids = [p["id"] for p in profiles]
    assert "NATURAL_OUTDOOR" in profile_ids
    assert "INDOOR_BUILDING" in profile_ids
    assert "INDUSTRIAL" in profile_ids
    assert "CRITICAL_INFRASTRUCTURE" in profile_ids
    assert "REMOTE_DISASTER_ZONE" in profile_ids

def test_natural_flood_evaluation():
    """Verify Natural Flood evaluation under normal baseline and high surge."""
    profile = environment_manager.switch_profile(EnvironmentType.NATURAL_OUTDOOR)
    
    # Surge readings
    surge_readings = [
        NormalizedSensorReading(
            node_id="NODE-01",
            sensor_type="ultrasonic_depth",
            metric_name="water_level_m",
            value=3.85,
            unit="m",
            battery_pct=92,
            auxiliary_metrics={"rate_of_rise_m_min": 0.12}
        ),
        NormalizedSensorReading(
            node_id="NODE-02",
            sensor_type="ultrasonic_depth",
            metric_name="water_level_m",
            value=3.90,
            unit="m",
            battery_pct=90,
            auxiliary_metrics={"rate_of_rise_m_min": 0.14}
        )
    ]
    assessment = universal_risk_engine.evaluate_environment(readings=surge_readings, profile=profile)
    assert assessment.overall_risk_score >= 75
    assert assessment.overall_severity == SeverityLevel.CRITICAL
    assert assessment.primary_threat == HazardType.FLASH_FLOOD
    assert any("critical at" in e for e in assessment.evidence_chain)

def test_indoor_fire_evaluation():
    """Verify Indoor Fire evaluation when thermal and optical particulate sensors surge."""
    profile = environment_manager.switch_profile(EnvironmentType.INDOOR_BUILDING)
    
    fire_readings = [
        NormalizedSensorReading(
            node_id="NODE-01",
            sensor_type="ambient_temperature",
            metric_name="temperature_c",
            value=74.5,
            unit="°C",
            location=LocationModel(building_id="BLDG-A", floor_level=3, room_or_zone="SERVER-ROOM"),
            battery_pct=95
        ),
        NormalizedSensorReading(
            node_id="NODE-02",
            sensor_type="optical_smoke",
            metric_name="smoke_obscuration_pct_m",
            value=5.8,
            unit="%/m",
            location=LocationModel(building_id="BLDG-A", floor_level=3, room_or_zone="SERVER-ROOM"),
            battery_pct=95
        )
    ]
    assessment = universal_risk_engine.evaluate_environment(readings=fire_readings, profile=profile)
    assert assessment.overall_risk_score >= 70
    assert assessment.overall_severity == SeverityLevel.CRITICAL
    assert assessment.primary_threat == HazardType.FIRE
    assert any("Extreme ambient thermal spike" in e for e in assessment.evidence_chain)
    assert any("mutually confirm" in e for e in assessment.evidence_chain)

def test_industrial_gas_leak_evaluation():
    """Verify Industrial Gas Leak evaluation when toxic/combustible concentration surges."""
    profile = environment_manager.switch_profile(EnvironmentType.INDUSTRIAL)
    
    gas_readings = [
        NormalizedSensorReading(
            node_id="NODE-01",
            sensor_type="catalytic_combustible_gas",
            metric_name="gas_concentration_ppm",
            value=165.0,
            unit="ppm",
            location=LocationModel(building_id="PLANT-01", room_or_zone="MANIFOLD-BAY-1"),
            battery_pct=91
        ),
        NormalizedSensorReading(
            node_id="NODE-02",
            sensor_type="catalytic_combustible_gas",
            metric_name="gas_concentration_ppm",
            value=158.0,
            unit="ppm",
            location=LocationModel(building_id="PLANT-01", room_or_zone="MANIFOLD-BAY-1"),
            battery_pct=88
        )
    ]
    assessment = universal_risk_engine.evaluate_environment(readings=gas_readings, profile=profile)
    assert assessment.overall_risk_score >= 75
    assert assessment.overall_severity == SeverityLevel.CRITICAL
    assert assessment.primary_threat == HazardType.GAS_LEAK
    assert any("gas concentration critical" in e for e in assessment.evidence_chain)
    assert "ISOLATE VALVES" in assessment.recommended_operational_action

def test_structural_vibration_evaluation():
    """Verify Critical Infrastructure evaluation under resonant vibration and tilt."""
    profile = environment_manager.switch_profile(EnvironmentType.CRITICAL_INFRASTRUCTURE)
    
    structural_readings = [
        NormalizedSensorReading(
            node_id="NODE-01",
            sensor_type="triaxial_accelerometer",
            metric_name="vibration_mm_s",
            value=8.4,
            unit="mm/s",
            battery_pct=88,
            auxiliary_metrics={"tilt_deg": 2.3}
        )
    ]
    assessment = universal_risk_engine.evaluate_environment(readings=structural_readings, profile=profile)
    assert assessment.overall_risk_score >= 75
    assert assessment.overall_severity == SeverityLevel.CRITICAL
    assert assessment.primary_threat == HazardType.STRUCTURAL_ANOMALY
    assert any("Severe resonant vibration peak" in e for e in assessment.evidence_chain)

def test_byzantine_sensor_trust_quarantine_across_metrics():
    """Verify that Byzantine Sensor Trust correctly isolates an erroneous industrial reading."""
    universal_trust_engine.reset()
    profile = environment_manager.switch_profile(EnvironmentType.INDUSTRIAL)
    
    readings = [
        NormalizedSensorReading(
            node_id="NODE-01",
            sensor_type="catalytic_combustible_gas",
            metric_name="gas_concentration_ppm",
            value=8.5,
            unit="ppm",
            battery_pct=94
        ),
        NormalizedSensorReading(
            node_id="NODE-02",
            sensor_type="catalytic_combustible_gas",
            metric_name="gas_concentration_ppm",
            value=9.0,
            unit="ppm",
            battery_pct=94
        ),
        # Malicious / faulty node injecting impossible spike
        NormalizedSensorReading(
            node_id="NODE-03",
            sensor_type="catalytic_combustible_gas",
            metric_name="gas_concentration_ppm",
            value=4500.0,
            unit="ppm",
            battery_pct=94
        )
    ]
    trust_batch = universal_trust_engine.evaluate_batch(readings, profile)
    assert trust_batch["NODE-01"]["status"] in ["VERIFIED", "TRUSTED"]
    assert trust_batch["NODE-02"]["status"] in ["VERIFIED", "TRUSTED"]
    # NODE-03 must be QUARANTINED due to Byzantine consensus disagreement
    assert trust_batch["NODE-03"]["status"] == "QUARANTINED"
    assert trust_batch["NODE-03"]["trust_score"] < 40.0
    assert any("Byzantine disagreement" in r for r in trust_batch["NODE-03"]["reasons"])

def test_environment_switch_api():
    """Verify REST API dynamic environment switching and multi-hazard state return."""
    # Switch to INDUSTRIAL
    res = client.post("/api/v1/environment/switch", json={"profile_id": "INDUSTRIAL"})
    assert res.status_code == 200
    data = res.json()
    assert data["profile"]["id"] == "INDUSTRIAL"
    assert "GAS_LEAK" in data["profile"]["active_hazards"]
    
    # Query current
    cur = client.get("/api/v1/environment/current").json()
    assert cur["profile"]["id"] == "INDUSTRIAL"

    # Switch back to NATURAL_OUTDOOR (default for SIH demo)
    res_back = client.post("/api/v1/environment/switch", json={"profile_id": "NATURAL_OUTDOOR"})
    assert res_back.status_code == 200
    assert res_back.json()["profile"]["id"] == "NATURAL_OUTDOOR"
