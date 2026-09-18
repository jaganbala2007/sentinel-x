"""
Sentinel-X Unit Tests: Core Engines
===================================
Tests sensor abstraction, Byzantine trust engine, anomaly detection,
multi-sensor fusion, and autonomous response logic.
"""

import unittest
from core.sensor_abstraction import SensorReading, SensorTrustStatus, SensorDataSource
from core.trust_engine import TrustEngine
from core.anomaly_engine import anomaly_engine
from core.fusion_engine import fusion_engine
from core.response_engine import response_engine, ResponseActionType
from core.event_engine import event_engine

class TestCoreEngines(unittest.TestCase):
    def test_sensor_reading_plausibility(self):
        sr = SensorReading(
            sensor_id="PT100_01",
            parameter="motor_temperature",
            value=75.0,
            unit="°C",
            min_physical_limit=-20.0,
            max_physical_limit=150.0,
            data_source=SensorDataSource.LIVE
        )
        self.assertTrue(sr.is_physically_plausible())
        self.assertIsNotNone(sr.calculate_checksum())

    def test_trust_engine_temporal_jump(self):
        engine = TrustEngine()
        engine.record_reading("PT100_01", 60.0)
        # Normal jump
        ok, _ = engine.check_temporal_consistency("PT100_01", 62.0, max_jump_per_sec=10.0)
        self.assertTrue(ok)

    def test_anomaly_detection_bounds_and_rate(self):
        res = anomaly_engine.evaluate("PT100_01", 160.0, min_limit=0.0, max_limit=140.0)
        self.assertTrue(res.is_anomaly)
        self.assertEqual(res.anomaly_type, "OUT_OF_BOUNDS")

    def test_multi_sensor_fusion_excludes_quarantined(self):
        s1 = SensorReading(sensor_id="S1", parameter="temp", value=70.0, unit="°C", trust_score=95.0, trust_status=SensorTrustStatus.TRUSTED, voting_weight=1.0)
        s2 = SensorReading(sensor_id="S2", parameter="temp", value=72.0, unit="°C", trust_score=90.0, trust_status=SensorTrustStatus.TRUSTED, voting_weight=1.0)
        s_spoof = SensorReading(sensor_id="S3", parameter="temp", value=140.0, unit="°C", trust_score=10.0, trust_status=SensorTrustStatus.QUARANTINED, voting_weight=0.0)

        fused = fusion_engine.fuse_readings("temp", [s1, s2, s_spoof])
        self.assertIn("S3", fused.quarantined_sensors)
        self.assertNotIn("S3", fused.contributing_sensors)
        # Fused value should be around 71°C, unaffected by the 140°C outlier
        self.assertAlmostEqual(fused.fused_value, 70.97, delta=1.5)

    def test_autonomous_response_critical_trip(self):
        actions = response_engine.evaluate_response("CRITICAL", "Worker Danger Intrusion", {})
        action_types = [a.action_type for a in actions]
        self.assertIn(ResponseActionType.EMERGENCY_STOP, action_types)
        self.assertIn(ResponseActionType.WARNING_BEACON, action_types)
        self.assertIn(ResponseActionType.EVACUATION_ALARM, action_types)

    def test_event_engine_correlation(self):
        evt = event_engine.create_event("INDUSTRIAL", "EQUIPMENT", 68.0, "WARNING", {"detail": "bearing wear"})
        self.assertTrue(evt.event_id.startswith("EVT-"))
        self.assertEqual(evt.sequence_num, 1)

if __name__ == "__main__":
    unittest.main()
