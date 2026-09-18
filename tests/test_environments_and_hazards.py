"""
Sentinel-X Unit Tests: Environments & Hazard Modules
====================================================
Validates environment-agnostic decoupling and domain-specific hazard modules.
"""

import unittest
from environments import environment_registry, industrial_profile, natural_profile
from hazards.equipment import equipment_hazard_module
from hazards.heat import heat_hazard_module
from hazards.worker_safety import worker_safety_hazard_module
from hazards.fire import fire_gas_hazard_module, flood_hazard_module
from hazards import hazard_engine

class TestEnvironmentsAndHazards(unittest.TestCase):
    def test_environment_registry_profiles(self):
        profiles = environment_registry.list_profiles()
        self.assertGreaterEqual(len(profiles), 6)
        types = [p["type"] for p in profiles]
        self.assertIn("INDUSTRIAL", types)
        self.assertIn("NATURAL", types)
        self.assertIn("INDOOR", types)

    def test_environment_switching(self):
        self.assertTrue(environment_registry.set_active_profile("NATURAL"))
        active = environment_registry.get_active_profile()
        self.assertEqual(active.type, "NATURAL")
        # Reset back to flagship
        environment_registry.set_active_profile("INDUSTRIAL")
        self.assertEqual(environment_registry.get_active_profile().type, "INDUSTRIAL")

    def test_equipment_hazard_iso10816(self):
        # Good vibration
        good = equipment_hazard_module.evaluate(1.8, 65.0, 60.0, 2.2)
        self.assertEqual(good.severity_level, "NORMAL")
        # Severe vibration (Zone D)
        bad = equipment_hazard_module.evaluate(8.2, 98.0, 75.0, 2.2)
        self.assertEqual(bad.severity_level, "CRITICAL")

    def test_heat_hazard_stator_breakdown(self):
        norm = heat_hazard_module.evaluate(68.0)
        self.assertEqual(norm.severity_level, "NORMAL")
        crit = heat_hazard_module.evaluate(99.0)
        self.assertEqual(crit.severity_level, "CRITICAL")

    def test_worker_safety_conflict(self):
        # Conveyor running (belt_speed=2.2) and worker enters nip zone (<0.9m)
        conflict = worker_safety_hazard_module.evaluate(worker_proximity_m=0.6, belt_speed=2.2)
        self.assertEqual(conflict.severity_level, "CRITICAL")
        self.assertTrue(conflict.conflict_detected)

    def test_flood_hazard_hydrology(self):
        norm_flood = flood_hazard_module.evaluate_flood(4.5, 10.0)
        self.assertEqual(norm_flood.severity_level, "NORMAL")
        danger_flood = flood_hazard_module.evaluate_flood(14.2, 120.0)
        self.assertEqual(danger_flood.severity_level, "CRITICAL")

    def test_unified_hazard_engine(self):
        eval_result = hazard_engine.evaluate_all({
            "motor_temperature": 70.0,
            "bearing_vibration": 2.2,
            "worker_proximity": 4.0,
            "smoke_gas_ppm": 15.0
        })
        self.assertEqual(eval_result["overall_severity"], "NORMAL")

if __name__ == "__main__":
    unittest.main()
