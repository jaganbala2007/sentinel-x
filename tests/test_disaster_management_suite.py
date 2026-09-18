"""
Sentinel-X Comprehensive Disaster Management Unit & Integration Test Suite
===========================================================================
Validates explainable risk scoring, multi-sensor correlation, disaster state machine,
hazard zone mapping, evacuation & resource manager, post-disaster recovery engine,
and SIH PS 26223 REST API endpoints.
"""

import sys
import os
import unittest
from datetime import datetime, timezone

# Add backend and workspace root to path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
_app_dir = os.path.join(_backend_dir, "backend")
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

from backend.app.services.disaster_risk_engine import risk_engine
from backend.app.services.multi_sensor_correlation import correlation_engine
from backend.app.services.disaster_state_machine import disaster_state_machine
from backend.app.services.zone_manager import zone_manager
from backend.app.services.evacuation_manager import evacuation_manager
from backend.app.services.post_disaster_engine import post_disaster_engine
from backend.app.services.scenario_engine import scenario_engine
from backend.app.services.twin_state_manager import twin_state_manager


class TestDisasterManagementSuite(unittest.TestCase):

    def test_01_explainable_risk_engine(self):
        """Test dynamic risk scoring formula and factor attribution breakdown."""
        nominal_telemetry = {"gas": 400, "temperature": 25.0, "vibration": 0.5, "trustScore": 100}
        res_norm = risk_engine.calculate_risk(nominal_telemetry)
        self.assertLess(res_norm["risk_score"], 30)
        self.assertEqual(res_norm["risk_level"], "NORMAL")

        critical_telemetry = {"gas": 2800, "temperature": 52.0, "vibration": 6.2, "trustScore": 100}
        res_crit = risk_engine.calculate_risk(critical_telemetry)
        self.assertGreaterEqual(res_crit["risk_score"], 80)
        self.assertEqual(res_crit["risk_level"], "CRITICAL")
        self.assertTrue(len(res_crit["contributors"]) >= 3)

    def test_02_multi_sensor_correlation_engine(self):
        """Test cross-sensor validation for fire, earthquake, and flood events."""
        node1 = {"gas": 2400, "temperature": 45.0, "trustScore": 100}
        node2 = {"gas": 2200, "temperature": 44.0, "vibration": 1.0, "trustScore": 100}
        res_fire = correlation_engine.evaluate_telemetry(node1, node2, "ONLINE")
        self.assertEqual(res_fire["event_type"], "FIRE_SMOKE_HAZARD")
        self.assertEqual(res_fire["severity"], "CRITICAL")
        self.assertGreaterEqual(res_fire["confidence"], 80)

        node_vib = {"gas": 400, "temperature": 25.0, "trustScore": 100}
        node_vib2 = {"vibration": 6.5, "trustScore": 100}
        res_eq = correlation_engine.evaluate_telemetry(node_vib, node_vib2, "ONLINE")
        self.assertEqual(res_eq["event_type"], "EARTHQUAKE_STRUCTURAL_VIBRATION")
        self.assertEqual(res_eq["severity"], "CRITICAL")

    def test_03_disaster_state_machine(self):
        """Test formal state machine transitions."""
        dsm = disaster_state_machine
        dsm.current_state = "NORMAL"
        rec = dsm.transition_to("WARNING", "Test warning breach", "COMMANDER")
        self.assertEqual(dsm.current_state, "WARNING")
        self.assertEqual(rec["newState"], "WARNING")

        rec2 = dsm.transition_to("CRITICAL", "Test critical breach", "COMMANDER")
        self.assertEqual(dsm.current_state, "CRITICAL")

        rec3 = dsm.transition_to("RESPONSE", "Commander dispatched teams", "COMMANDER")
        self.assertEqual(dsm.current_state, "RESPONSE")

    def test_04_zone_manager(self):
        """Test zone hazard status updates and color mapping."""
        z = zone_manager.update_zone_status("ZONE_B", "CRITICAL", 3, "EVACUATE")
        self.assertEqual(z["status"], "CRITICAL")
        self.assertEqual(z["color"], "RED")
        self.assertEqual(z["evacuationStatus"], "EVACUATE")

        all_zones = zone_manager.get_all_zones()
        self.assertEqual(all_zones["totalZones"], 4)

    def test_05_evacuation_and_resources(self):
        """Test spatial evacuation triggers and resource allocations."""
        evac_state = evacuation_manager.trigger_evacuation("ZONE_B")
        self.assertTrue(evac_state["evacuationModeActive"])
        self.assertIn("ZONE_B", evac_state["affectedZones"])

        res = evacuation_manager.assign_resource("RES-01", "INC-TEST-1")
        self.assertEqual(res["status"], "DEPLOYED")
        self.assertEqual(res["assignedIncident"], "INC-TEST-1")

        evacuation_manager.reset_evacuation()
        self.assertFalse(evacuation_manager.evacuation_mode_active)

    def test_06_post_disaster_engine(self):
        """Test post-disaster recovery report generation and performance metrics."""
        inc = {"id": "INC-TEST-100", "zone": "ZONE_B", "disaster_type": "FIRE_SMOKE_HAZARD", "severity": "CRITICAL"}
        report = post_disaster_engine.generate_recovery_report(inc, [])
        self.assertEqual(report["report_id"], "RPT-INC-TEST-100")
        self.assertIn("metrics", report)
        self.assertEqual(report["metrics"]["total_recovery_time_min"], 7.1)
        self.assertTrue(len(report["actions_taken"]) >= 4)

    def test_07_scenario_engine(self):
        """Test deterministic scenario simulator step generation."""
        scenarios = scenario_engine.get_available_scenarios()
        self.assertGreaterEqual(len(scenarios), 5)

        step_data = scenario_engine.get_step_telemetry("FIRE_SMOKE", 3)
        self.assertEqual(step_data["scenario_id"], "FIRE_SMOKE")
        self.assertEqual(step_data["step_index"], 3)
        self.assertGreater(step_data["telemetry"]["gas"], 2000)

    def test_08_twin_state_manager_authoritative_state(self):
        """Test authoritative state dictionary contents."""
        state = twin_state_manager.get_authoritative_state()
        self.assertEqual(state["system"], "SENTINEL-X")
        self.assertIn("disasterLifecycleState", state)
        self.assertIn("zones", state)
        self.assertIn("evacuation", state)


if __name__ == "__main__":
    unittest.main()
