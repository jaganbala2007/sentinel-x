"""
Sentinel-X Unit Tests: Hardware Abstraction & Storage
=====================================================
Validates edge intelligence unit, USB pendrive WAL persistence,
ESP32 telemetry labeling, and local actuator interlocks.
"""

import unittest
import os
from hardware.raspberry_pi import raspberry_pi_manager
from hardware.pendrive import usb_pendrive_store
from hardware.esp32 import esp32_fleet_manager
from hardware.actuators import actuator_manager
from storage.database import get_connection, DEFAULT_DB_PATH
from storage.pendrive_store import pendrive_manager

class TestHardwareAndStorage(unittest.TestCase):
    def test_rpi5_metrics(self):
        status = raspberry_pi_manager.get_status()
        self.assertEqual(status.device_id, "RPI5-EDGE-01")
        self.assertTrue(status.local_autonomy_guaranteed)
        self.assertLess(status.local_decision_latency_ms, 20.0)

    def test_sqlite_wal_mode_active(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        mode = cursor.fetchone()[0].lower()
        conn.close()
        self.assertEqual(mode, "wal")

    def test_esp32_fleet_provenance(self):
        nodes = esp32_fleet_manager.get_all_nodes()
        self.assertGreaterEqual(len(nodes), 4)
        for n in nodes:
            self.assertIn(n.data_source, ["LIVE", "SIMULATED", "INFERRED", "OFFLINE", "PLANNED"])

    def test_actuator_emergency_trip(self):
        actuator_manager.set_nominal()
        self.assertTrue(actuator_manager.get_state().conveyor_motor_relay)
        self.assertEqual(actuator_manager.get_state().warning_beacon_color, "GREEN")

        actuator_manager.trigger_emergency_interlock("Simulated Trip")
        self.assertFalse(actuator_manager.get_state().conveyor_motor_relay)
        self.assertEqual(actuator_manager.get_state().warning_beacon_color, "RED")
        self.assertEqual(actuator_manager.get_state().siren_db, 95)

    def test_pendrive_offline_store_and_sync(self):
        test_event = {
            "event_id": "TEST-EVT-001",
            "source": "TEST",
            "environment": "INDUSTRIAL",
            "hazard": "MECHANICAL",
            "risk_score": 75.0,
            "priority": "HIGH",
            "payload": {"test": True}
        }
        success = pendrive_manager.persist_event_offline(test_event)
        self.assertTrue(success)

        # Mark synced
        pendrive_manager.mark_event_synced("TEST-EVT-001")
        status = pendrive_manager.get_status()
        self.assertTrue(status.mounted)

if __name__ == "__main__":
    unittest.main()
