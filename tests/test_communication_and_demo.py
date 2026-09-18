"""
Sentinel-X Unit Tests: Communication Resilience & SIH 23-Step Demo
==================================================================
Tests communication failovers, HF/Satellite simulation, and all 23 demo steps.
"""

import unittest
from communication.manager import communication_manager, CommunicationState, TransportChannel
from communication.mqtt_adapter import mqtt_adapter
from communication.hf_simulator import hf_packet_simulator
from communication.satellite_adapter import satellite_adapter
from communication.store_forward import store_and_forward_manager
from digital_twin.sih_demo import sih_demo_engine
from digital_twin.scene import get_flagship_industrial_scene
from digital_twin.reconstruction import reconstructor

class TestCommunicationAndDemo(unittest.TestCase):
    def test_communication_failover_cycle(self):
        # 1. Normal
        communication_manager.set_state(CommunicationState.NORMAL)
        self.assertEqual(communication_manager.get_status().active_channel, TransportChannel.INTERNET_WAN)

        # 2. Degraded -> Local LAN
        communication_manager.set_state(CommunicationState.DEGRADED)
        self.assertEqual(communication_manager.get_status().active_channel, TransportChannel.LOCAL_MQTT)

        # 3. Emergency -> HF Radio
        communication_manager.set_state(CommunicationState.EMERGENCY)
        self.assertEqual(communication_manager.get_status().active_channel, TransportChannel.HF_PACKET_RADIO)

        # 4. Isolated -> Offline Pendrive
        communication_manager.set_state(CommunicationState.ISOLATED)
        self.assertEqual(communication_manager.get_status().active_channel, TransportChannel.OFFLINE_PENDRIVE)

        # 5. Recovery
        communication_manager.set_state(CommunicationState.RECOVERY)
        self.assertEqual(communication_manager.get_status().active_channel, TransportChannel.INTERNET_WAN)

    def test_hf_radio_packet_simulation(self):
        success, packet = hf_packet_simulator.transmit_event({"source": "RPI5", "risk_score": 85.0})
        self.assertTrue(packet.crc16.startswith("0x"))
        self.assertGreater(packet.sequence_num, 0)

    def test_satellite_sbd_simulation(self):
        sbd = satellite_adapter.transmit_burst({"event_id": "EVT-99", "hazard": "HEAT", "risk_score": 75})
        self.assertEqual(sbd.constellation, "IRIDIUM_LEO")
        self.assertIsNotNone(sbd.payload_hex)

    def test_store_and_forward_enqueue_and_sync(self):
        ok = store_and_forward_manager.enqueue_event({
            "event_id": "EVT-TEST-SF",
            "source": "RPI5",
            "hazard": "MECHANICAL",
            "risk_score": 65.0
        })
        self.assertTrue(ok)
        stats = store_and_forward_manager.get_stats()
        self.assertEqual(stats.status_label, "STORE-AND-FORWARD ACTIVE")

    def test_sih_demo_all_23_steps(self):
        """Verifies every single step of the 27-step demonstration sequence."""
        for step_num in range(1, 28):
            state = sih_demo_engine.get_step_state(step_num)
            self.assertEqual(state.step_number, step_num)
            self.assertIsNotNone(state.title)
            self.assertIn(state.risk_level, ["NORMAL", "WATCH", "WARNING", "CRITICAL"])
            self.assertIn(state.communication_state, ["NORMAL", "DEGRADED", "EMERGENCY", "ISOLATED", "RECOVERY"])

        # Check key specific steps
        step_norm = sih_demo_engine.get_step_state(1)
        self.assertEqual(step_norm.risk_level, "NORMAL")

        step_spoof = sih_demo_engine.get_step_state(9)
        self.assertIn("SENSOR_TEMP_AUX_B", step_spoof.quarantined_sensors)

        step_trip = sih_demo_engine.get_step_state(11)
        self.assertEqual(step_trip.risk_level, "CRITICAL")
        self.assertTrue(step_trip.actuators["e_stop"])

        step_iso = sih_demo_engine.get_step_state(14)
        self.assertEqual(step_iso.communication_state, "ISOLATED")

        step_rec = sih_demo_engine.get_step_state(17)
        self.assertEqual(step_rec.communication_state, "RECOVERY")

        step_final = sih_demo_engine.get_step_state(27)
        self.assertEqual(step_final.step_number, 27)

    def test_flagship_industrial_scene(self):
        scene = get_flagship_industrial_scene()
        self.assertEqual(scene.scene_type, "FLAGSHIP_CONVEYOR_3D_SCADA")
        obj_ids = [o.object_id for o in scene.objects]
        self.assertIn("OBJ_MOTOR_01", obj_ids)
        self.assertIn("OBJ_GEARBOX_01", obj_ids)
        self.assertIn("OBJ_CONVEYOR_BELT", obj_ids)
        self.assertIn("OBJ_RESTRICTED_ZONE", obj_ids)

    def test_photo_reconstruction_pipeline(self):
        job = reconstructor.reconstruct_from_photos(["photo1.jpg", "photo2.jpg", "photo3.jpg"])
        self.assertEqual(job.status, "COMPLETED")
        self.assertGreater(len(job.detected_assets), 3)

if __name__ == "__main__":
    unittest.main()
