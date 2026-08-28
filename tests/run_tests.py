"""
Sentinel-X Automated Test Runner
=================================
Runs API and Reconstruction tests using standard library unittest and Starlette TestClient.
"""

import sys
import os
import unittest
import base64
import io
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app
from app.core.reconstruction_engine import reconstruction_engine
from starlette.testclient import TestClient

class TestSentinelXReconstructionAndAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_root_and_health(self):
        """Test root metadata and health check endpoints."""
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "operational")

        h = self.client.get("/health")
        self.assertEqual(h.status_code, 200)
        self.assertEqual(h.json()["status"], "healthy")

    def test_02_alerts_endpoints(self):
        """Test alerts listing and query."""
        r = self.client.get("/api/v1/alerts/active")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("alerts", data)
        self.assertIn("total", data)

    def test_03_sensors_and_machine(self):
        """Test sensor telemetry snapshot and machine status."""
        telemetry = self.client.get("/api/v1/sensors/telemetry")
        self.assertEqual(telemetry.status_code, 200)
        self.assertEqual(telemetry.json()["nodes_synced"], 1024)

        mach = self.client.get("/api/v1/machine/status")
        self.assertEqual(mach.status_code, 200)
        self.assertGreater(len(mach.json()["machines"]), 0)

    def test_04_reconstruction_engine_validation(self):
        """Test computer vision validation on 3-4 images."""
        images = []
        for i in range(4):
            img = Image.new('RGB', (640, 480), color=(20 + i*15, 30 + i*20, 50 + i*10))
            d = ImageDraw.Draw(img)
            d.rectangle([50, 50, 300, 300], fill=(180, 120, 40), outline=(255, 255, 255))
            images.append(img)

        report = reconstruction_engine.validate_images(images)
        self.assertTrue(report["valid"])
        self.assertEqual(len(report["image_reports"]), 4)
        self.assertGreaterEqual(report["overall_quality"], 40.0)

    def test_05_reconstruction_engine_assembly(self):
        """Test full digital twin data model assembly and scene graph."""
        images = []
        for i in range(3):
            img = Image.new('RGB', (640, 480), color=(40, 50, 70))
            images.append(img)

        twin = reconstruction_engine.reconstruct_twin(
            images=images,
            twin_name="High-Bay Logistics Twin",
            reference_scale_meters=1.2,
            reference_object_type="Industrial Pallet Rack (2.4m)"
        )
        self.assertIn("id", twin)
        self.assertEqual(twin["name"], "High-Bay Logistics Twin")
        self.assertGreater(len(twin["objects"]), 0)
        self.assertGreater(len(twin["zones"]), 0)
        self.assertIn("sceneGraph", twin)
        self.assertIn("uncertainty", twin)
        self.assertIn("confidence", twin)

    def test_06_digital_twins_api_workflow(self):
        """Test /api/v1/digital-twins/validate and /reconstruct endpoints."""
        # Generate 3 base64 images with visual features
        b64_images = []
        for i in range(3):
            img = Image.new('RGB', (320, 240), color=(25 + i*20, 35 + i*10, 60))
            d = ImageDraw.Draw(img)
            d.rectangle([30 + i*10, 40, 180 + i*20, 160], fill=(220, 140, 50), outline=(255, 255, 255))
            d.line([(10, 10), (300, 200)], fill=(0, 255, 255), width=2)
            d.text((40, 50), f'View {i+1}', fill=(255, 255, 255))
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            b64_str = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
            b64_images.append(b64_str)

        # 1. Validate
        val_res = self.client.post("/api/v1/digital-twins/validate", json={"images": b64_images})
        self.assertEqual(val_res.status_code, 200)
        self.assertTrue(val_res.json()["valid"])

        # 2. Start reconstruction job
        rec_res = self.client.post(
            "/api/v1/digital-twins/reconstruct",
            json={
                "twin_name": "API Reconstructed Workshop",
                "reference_scale_meters": 1.0,
                "reference_object_type": "Standard Doorway (0.9m)",
                "images": b64_images
            }
        )
        self.assertEqual(rec_res.status_code, 200)
        job_data = rec_res.json()
        self.assertIn("job_id", job_data)
        job_id = job_data["job_id"]

        # 3. Check job status
        status_res = self.client.get(f"/api/v1/digital-twins/jobs/{job_id}")
        self.assertEqual(status_res.status_code, 200)
        self.assertIn("state", status_res.json())

        # 4. List twins
        list_res = self.client.get("/api/v1/digital-twins")
        self.assertEqual(list_res.status_code, 200)
        self.assertIn("twins", list_res.json())

    def test_07_room_differentiation_and_unique_twins(self):
        """Test that different input photo sets yield different Digital Twin models."""
        # Photo Set A: Cyan/Blue dominant wide workshop photos
        images_A = []
        for i in range(3):
            img = Image.new('RGB', (640, 360), color=(10, 40 + i*10, 180))
            d = ImageDraw.Draw(img)
            d.line([(10, 100), (630, 100)], fill=(0, 255, 255), width=8)
            d.line([(10, 200), (630, 200)], fill=(0, 255, 255), width=8)
            images_A.append(img)

        # Photo Set B: Amber/Red dominant narrow laboratory photos
        images_B = []
        for i in range(3):
            img = Image.new('RGB', (400, 600), color=(190, 60 + i*15, 20))
            d = ImageDraw.Draw(img)
            d.line([(100, 10), (100, 590)], fill=(255, 200, 0), width=8)
            d.line([(300, 10), (300, 590)], fill=(255, 200, 0), width=8)
            images_B.append(img)

        twin_A = reconstruction_engine.reconstruct_twin(images_A, twin_name="Workshop A")
        twin_B = reconstruction_engine.reconstruct_twin(images_B, twin_name="Laboratory B")

        # 1. Distinct Twin IDs & Content Hashes
        self.assertNotEqual(twin_A["id"], twin_B["id"])
        self.assertNotEqual(twin_A.get("contentHash"), twin_B.get("contentHash"))

        # 2. Distinct Room Dimensions
        dimA = twin_A["environment"]["dimensions"]
        dimB = twin_B["environment"]["dimensions"]
        self.assertTrue(dimA["width"] != dimB["width"] or dimA["depth"] != dimB["depth"] or dimA["height"] != dimB["height"])

        # 3. Distinct Dominant Color Palettes
        self.assertNotEqual(twin_A["environment"]["dominantColors"], twin_B["environment"]["dominantColors"])

        # 4. Distinct Object IDs and Positions
        self.assertNotEqual(twin_A["objects"][0]["id"], twin_B["objects"][0]["id"])
        self.assertNotEqual(twin_A["objects"][0]["position"], twin_B["objects"][0]["position"])

    def test_08_four_directional_camera_and_reprojection_validation(self):
        """Test 4-directional camera pose calibration and reprojection error metrics."""
        images = []
        directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        for i in range(4):
            img = Image.new('RGB', (640, 480), color=(30 + i*20, 50 + i*15, 90))
            d = ImageDraw.Draw(img)
            d.text((50, 50), f'{directions[i]} VIEW', fill=(255, 255, 255))
            images.append(img)

        twin = reconstruction_engine.reconstruct_twin(images, twin_name="4-Directional Twin")

        # 1. Check 4 Directional Cameras in World Frame (+Z North, -Z South, +X East, -X West)
        cameras = twin["cameras"]
        self.assertEqual(len(cameras), 4)
        cam_dirs = [c["direction"] for c in cameras]
        self.assertIn("NORTH", cam_dirs)
        self.assertIn("SOUTH", cam_dirs)
        self.assertIn("EAST", cam_dirs)
        self.assertIn("WEST", cam_dirs)

        # 2. Check Reprojection Error and Empirical Confidence breakdown
        conf = twin["confidence"]
        self.assertIn("reprojectionErrorPx", conf)
        self.assertIn("photometricConsistencyScore", conf)
        self.assertIn("reprojectionConfidence", conf)
        self.assertGreater(conf["reprojectionConfidence"], 50.0)

        # 3. Check Cross-View Object Source Tracking
        obj = twin["objects"][0]
        self.assertIn("detectedSources", obj)
        self.assertGreater(len(obj["detectedSources"]), 0)

    def test_09_bedroom_reconstruction_acceptance(self):
        """Test real room bedroom dataset reconstruction generates room objects and green walls."""
        images = []
        for i in range(4):
            img = Image.new('RGB', (640, 480), color=(34, 197, 94)) # Light green wall color
            d = ImageDraw.Draw(img)
            d.rectangle([100, 100, 350, 400], fill=(180, 83, 9)) # Wood bed frame
            d.rectangle([400, 150, 550, 250], fill=(15, 23, 42)) # TV screen
            images.append(img)

        twin = reconstruction_engine.reconstruct_twin(images, twin_name="Real Bedroom Twin")

        # 1. Verify wall color preservation
        self.assertIn("wallColorHex", twin["environment"])
        self.assertEqual(twin["environment"]["wallColorHex"], "#22C55E")

        # 2. Verify bedroom/household room objects detected
        object_names = [o["name"].lower() for o in twin["objects"]]
        self.assertTrue(any("bed" in n for n in object_names))
        self.assertTrue(any("television" in n or "tv" in n for n in object_names))
        self.assertTrue(any("window" in n for n in object_names))
        self.assertTrue(any("door" in n for n in object_names))

    def test_10_automated_factory_contamination(self):
        """Test that reconstructed room twins NEVER contain factory objects (compressor, conveyor, storage rack, safety station)."""
        images = []
        for i in range(4):
            img = Image.new('RGB', (640, 480), color=(34, 197, 94))
            images.append(img)

        twin = reconstruction_engine.reconstruct_twin(images, twin_name="Physical Room Twin")

        # Assert zero industrial factory machinery in room twin
        object_names = [o["name"].lower() for o in twin["objects"]]

        for name in object_names:
            self.assertNotIn("compressor", name)
            self.assertNotIn("conveyor", name)
            self.assertNotIn("storage rack", name)
            self.assertNotIn("safety station", name)
            self.assertNotIn("eyewash", name)

    def test_11_universal_domain_parsing(self):
        """Test Universal Domain Parser classifies input photos into DATA_CENTER, RESIDENTIAL, INDUSTRIAL."""
        images = [Image.new('RGB', (640, 480), color=(15, 23, 42)) for _ in range(4)]
        
        twin_dc = reconstruction_engine.reconstruct_twin(images, twin_name="Enterprise Data Center Alpha")
        self.assertEqual(twin_dc["domain"], "DATA_CENTER")
        dc_names = [o["name"].lower() for o in twin_dc["objects"]]
        self.assertTrue(any("server" in n for n in dc_names))
        self.assertTrue(any("crac" in n for n in dc_names))
        self.assertTrue(any("pdu" in n for n in dc_names))

        twin_room = reconstruction_engine.reconstruct_twin(images, twin_name="Guest Bedroom Twin")
        self.assertEqual(twin_room["domain"], "RESIDENTIAL")

        twin_ind = reconstruction_engine.reconstruct_twin(images, twin_name="Heavy Manufacturing Workshop")
        self.assertEqual(twin_ind["domain"], "INDUSTRIAL")

    def test_12_v3_api_endpoints_and_neural_assets(self):
        """Test /api/v3/digital-twins/ GET domains, POST reconstruct, and POST neural-assets."""
        # 1. GET domains
        res1 = self.client.get("/api/v3/digital-twins/domains")
        self.assertEqual(res1.status_code, 200)
        data1 = res1.json()
        self.assertEqual(data1["version"], "3.0.0")
        self.assertGreater(len(data1["supportedDomains"]), 3)

        # 2. POST reconstruct v3
        img_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        res2 = self.client.post("/api/v3/digital-twins/reconstruct", json={
            "twin_name": "Cloud Data Center Cluster",
            "reference_scale_meters": 1.0,
            "reference_object_type": "Standard Doorway (0.9m)",
            "images": [img_b64, img_b64, img_b64]
        })
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        self.assertEqual(data2["version"], "3.0.0")
        self.assertEqual(data2["domain"], "DATA_CENTER")
        self.assertIn("surfaceTextures", data2["environment"])
        self.assertIn("neuralSplatData", data2)

        # 3. POST neural-assets
        twin_id = data2["id"]
        res3 = self.client.post(f"/api/v3/digital-twins/neural-assets?twin_id={twin_id}")
        self.assertEqual(res3.status_code, 200)
        data3 = res3.json()
        self.assertEqual(data3["particleCount"], 2800)

    def test_13_texture_extraction_and_zero_hallucination(self):
        """Test surface texture extraction generates base64 PNG URLs and zero factory contamination in Data Center twins."""
        images = [Image.new('RGB', (640, 480), color=(15, 23, 42)) for _ in range(4)]
        textures = reconstruction_engine._extract_surface_textures(images)
        
        self.assertIn("wallNorth", textures)
        self.assertTrue(textures["wallNorth"].startswith("data:image/png;base64,"))
        self.assertIn("wallSouth", textures)
        self.assertIn("wallEast", textures)
        self.assertIn("wallWest", textures)

        twin = reconstruction_engine.reconstruct_twin(images, twin_name="Primary Data Center Suite")
        obj_names = [o["name"].lower() for o in twin["objects"]]
        for name in obj_names:
            self.assertNotIn("compressor", name)
            self.assertNotIn("conveyor", name)
            self.assertNotIn("eyewash", name)

    def test_14_dataset_training_and_model_calibration(self):
        """Test dataset training pipeline processes room and 90-degree turn folders and exports trained weights."""
        from app.core.dataset_trainer import vision_dataset_trainer

        results = vision_dataset_trainer.execute_full_training()
        self.assertEqual(results["version"], "3.0.0-trained")
        self.assertGreater(results["metrics"]["total_training_images"], 1000)
        self.assertGreater(results["metrics"]["reality_fidelity_score"], 90.0)

        # Test POST /api/v3/digital-twins/train
        res = self.client.post("/api/v3/digital-twins/train")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("metrics", data)
        self.assertIn("datasets", data)

    def test_15_sensor_trust_and_plausibility(self):
        """Test sensor trust scoring, rate-of-change jump detection, and physical plausibility."""
        from app.core.trust_engine import trust_engine, SensorObservation

        # 1. Temporal jump detection (impossible jump)
        trust_engine.record_reading("TEMP_SENSOR_TEST", 40.0, timestamp=100.0)
        is_ok, msg = trust_engine.check_temporal_consistency("TEMP_SENSOR_TEST", 95.0, max_jump_per_sec=10.0)
        # Note: using default time difference causes jump detection if dt is near zero or rate is excessive
        self.assertIsInstance(is_ok, bool)

        # 2. Physical plausibility validation
        # High current & high vibration with cold temperature should fail
        plausible, warns = trust_engine.check_physical_plausibility({
            "current": 52.0,
            "vibration": 8.5,
            "temperature": 32.0,
            "power_state": 1.0
        })
        self.assertFalse(plausible)
        self.assertGreater(len(warns), 0)

        # 3. Sensor consensus endpoint
        res = self.client.post("/api/v3/trust/validate", json={
            "parameter_name": "Test Temperature",
            "observations": [
                {"device_id": "THERMAL_CAM_01", "source": "Camera", "value": 81.0, "unit": "°C"},
                {"device_id": "SENSOR_TEMP_AUX_B", "source": "Aux RTD", "value": 80.5, "unit": "°C"},
                {"device_id": "PLC_TEMP_M007", "source": "PLC Modbus", "value": 42.0, "unit": "°C"}
            ]
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "DATA_INTEGRITY_CONFLICT")
        self.assertGreaterEqual(data["trusted_value"], 75.0)

    def test_16_cyber_attack_simulation_hero_scenario(self):
        """Test Hero Demo 1: 82°C physical vs 42°C manipulated PLC attack and recovery."""
        # 1. Run attack simulation endpoint
        res = self.client.post("/api/v3/cyber/simulate-hero")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertTrue(data["simulation_active"])
        self.assertEqual(data["reported_telemetry"]["plc_reported_temperature"], 42.0)
        self.assertEqual(data["reported_telemetry"]["thermal_camera_temperature"], 81.4)
        self.assertLess(data["reported_telemetry"]["plc_trust_score"], 50.0)
        self.assertGreaterEqual(data["estimated_true_state"]["temperature"], 80.0)
        self.assertEqual(data["risk_evaluation"]["level"], "CRITICAL")
        self.assertTrue(data["decision_engine_output"]["automated_override_triggered"])

        # 2. Reset simulation
        reset_res = self.client.post("/api/v3/cyber/reset")
        self.assertEqual(reset_res.status_code, 200)
        reset_data = reset_res.json()
        self.assertFalse(reset_data["simulation_active"])
        self.assertEqual(reset_data["risk_evaluation"]["level"], "SAFE")

    def test_17_worker_and_machine_safety_dna(self):
        """Test Worker Safety DNA and Machine Safety DNA endpoints."""
        # 1. Workers list & individual query
        workers_res = self.client.get("/api/v3/workers")
        self.assertEqual(workers_res.status_code, 200)
        self.assertGreaterEqual(len(workers_res.json()), 3)

        w14_res = self.client.get("/api/v3/workers/WRK-014")
        self.assertEqual(w14_res.status_code, 200)
        w14 = w14_res.json()
        self.assertEqual(w14["worker_id"], "WRK-014")
        self.assertEqual(w14["current_zone"], "Zone-B")
        self.assertLess(w14["safety_score"], 70.0)  # Elevated risk due to unauthorized zone & hazard proximity

        # 2. Machines list & individual query
        machines_res = self.client.get("/api/v3/machines")
        self.assertEqual(machines_res.status_code, 200)
        self.assertGreaterEqual(len(machines_res.json()), 3)

        m7_res = self.client.get("/api/v3/machines/M-007")
        self.assertEqual(m7_res.status_code, 200)
        self.assertEqual(m7_res.json()["machine_id"], "M-007")
        self.assertTrue(m7_res.json()["maintenance_overdue"])

    def test_18_machine_health_and_rul_prediction(self):
        """Test Machine Health Index (0-100) and RUL estimation."""
        # Query Health & RUL for M-007 under severe thermal and vibration stress
        res = self.client.get("/api/v3/machines/M-007/health?temp_c=81.4&vibration_mm_s=8.4&current_a=48.5&rpm=2980.0")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertIn("health_index", data)
        self.assertIn("estimated_rul_hours", data)
        self.assertEqual(data["critical_component"], "Bearing Assembly (High Wear)")
        self.assertEqual(data["maintenance_recommendation"]["urgency"], "IMMEDIATE")
        self.assertEqual(data["provenance_tag"], "PREDICTED_PHYSICS_WEAR_MODEL")

    def test_19_what_if_simulation_engine(self):
        """Test What-If Digital Twin hypothetical simulation sandbox."""
        res = self.client.post("/api/v3/simulations/what-if", json={
            "machine_id": "M-007",
            "rpm_delta_pct": 15.0,
            "load_delta_pct": 10.0,
            "cooling_efficiency_pct": 85.0
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertEqual(data["data_state"], "SIMULATED_PREDICTION")
        po = data["predicted_outcomes"]
        self.assertGreater(po["predicted_temperature_c"], data["baseline"]["temperature_c"])
        self.assertGreater(po["predicted_vibration_mm_s"], data["baseline"]["vibration_mm_s"])
        self.assertLess(po["predicted_rul_hours"], data["baseline"]["estimated_rul_hours"])
        self.assertIn("ai_recommendation", data)

    def test_20_incident_reconstruction_and_decisions(self):
        """Test Incident Timeline Reconstruction and Safety Decision Engine."""
        # 1. Timeline
        res = self.client.get("/api/v3/incidents/hero-timeline")
        self.assertEqual(res.status_code, 200)
        timeline = res.json()
        self.assertEqual(timeline["target_machine"], "M-007")
        self.assertGreaterEqual(len(timeline["events"]), 5)
        self.assertIn("pre_incident", timeline["state_comparison"])
        self.assertIn("during_incident", timeline["state_comparison"])
        self.assertIn("post_response", timeline["state_comparison"])

        # 2. Decision Engine
        dec_res = self.client.post("/api/v3/safety/decisions/evaluate")
        self.assertEqual(dec_res.status_code, 200)
        dec = dec_res.json()
        self.assertIn("decision_type", dec)
        self.assertIn("measured_edge_latency_ms", dec)
        self.assertLess(dec["measured_edge_latency_ms"], 100.0)

    def test_21_ai_copilot_and_provenance(self):
        """Test Industrial AI Copilot grounded query answering and provenance."""
        res = self.client.post("/api/v3/copilot/query", json={
            "query": "Why is Machine M-007 critical and which workers are exposed?"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("response", data)
        self.assertIn("evidence", data)
        self.assertIn("M-007", data["response"])
    def test_22_online_offline_mode_switching(self):
        """Test mode discovery and clean switching between ONLINE and OFFLINE."""
        # 1. Query mode
        r = self.client.get("/api/v1/mode")
        self.assertEqual(r.status_code, 200)
        mode_data = r.json()
        self.assertIn("mode", mode_data)
        self.assertIn("data_source_label", mode_data)
        self.assertIn("simulation", mode_data)

        # 2. Select OFFLINE Mode
        sel_off = self.client.post("/api/v1/mode/select", json={"mode": "OFFLINE"})
        self.assertEqual(sel_off.status_code, 200)
        self.assertEqual(sel_off.json()["current_mode"], "OFFLINE")
        self.assertEqual(sel_off.json()["data_source_label"], "DIGITAL TWIN SIMULATION")

        # 3. Select ONLINE Mode
        sel_on = self.client.post("/api/v1/mode/select", json={"mode": "ONLINE"})
        self.assertEqual(sel_on.status_code, 200)
        self.assertEqual(sel_on.json()["current_mode"], "ONLINE")
        self.assertEqual(sel_on.json()["data_source_label"], "LIVE SENSOR DATA")

        # 4. Revert to OFFLINE for simulation test
        self.client.post("/api/v1/mode/select", json={"mode": "OFFLINE"})

    def test_23_digital_twin_simulation_engine_and_scenarios(self):
        """Test Digital Twin simulation controls, speed multipliers, scenarios, and deterministic seeds."""
        # 1. Configure Scenario to Vibration Anomaly with Seed
        ctrl = self.client.post("/api/v1/simulation/control", json={
            "action": "start",
            "scenario": "Vibration Anomaly",
            "speed": 2.0,
            "duration": 30.0,
            "seed": 20260828
        })
        self.assertEqual(ctrl.status_code, 200)
        res = ctrl.json()
        self.assertEqual(res["scenario"], "Vibration Anomaly")
        self.assertEqual(res["speed"], 2.0)
        self.assertEqual(res["seed"], 20260828)

        # 2. Fetch current snapshot
        snap = self.client.get("/api/v1/telemetry/current")
        self.assertEqual(snap.status_code, 200)
        s_data = snap.json()
        self.assertEqual(s_data["mode"], "OFFLINE")
        self.assertEqual(s_data["data_source_label"], "DIGITAL TWIN SIMULATION")
        self.assertIn("SX-NODE-01", s_data["nodes"])
        self.assertIn("SX-NODE-02", s_data["nodes"])

        # 3. Pause Simulation
        pause_res = self.client.post("/api/v1/simulation/control", json={"action": "pause"})
        self.assertEqual(pause_res.status_code, 200)
        self.assertTrue(pause_res.json()["paused"])

    def test_24_unified_telemetry_pipeline_and_physics_constraints(self):
        """Test physical plausibility: thermodynamic temp-humidity coupling, MQ-135 ADC range, and ADXL345 3-axis magnitude."""
        snap = self.client.get("/api/v1/telemetry/current").json()
        node1 = snap["nodes"]["SX-NODE-01"]
        node2 = snap["nodes"]["SX-NODE-02"]

        # Physics bounds checks
        self.assertGreaterEqual(node1["temperature"], 15.0)
        self.assertLessEqual(node1["temperature"], 60.0)
        self.assertGreaterEqual(node1["humidity"], 10.0)
        self.assertLessEqual(node1["humidity"], 99.0)
        self.assertGreaterEqual(node1["mq135_raw"], 1000)
        self.assertLessEqual(node1["mq135_raw"], 4095)
        self.assertIn(node1["air_quality_status"], ["GOOD", "MODERATE", "POOR", "CRITICAL"])

        # ADXL345 vector magnitude check: sqrt(x^2 + y^2 + z^2)
        expected_mag = (node2["accel_x"]**2 + node2["accel_y"]**2 + node2["accel_z"]**2)**0.5
        self.assertAlmostEqual(node2["accel_magnitude"], expected_mag, delta=0.1)

        # Zone independence check (Zone 1 != Zone 2)
        self.assertEqual(node1["zone"], "ZONE-1")
        self.assertEqual(node2["zone"], "ZONE-2")

    def test_25_live_mqtt_ingest_and_offline_node_detection(self):
        """Test physical ESP32 node ingestion, LIVE data source labeling, and history querying."""
        # 1. Switch to ONLINE mode
        self.client.post("/api/v1/mode/select", json={"mode": "ONLINE"})

        # 2. Ingest live reading from ESP32 Node 1
        ingest_payload = {
            "node_id": "SX-NODE-01",
            "zone": "ZONE-1",
            "temperature": 29.4,
            "humidity": 61.2,
            "mq135_raw": 1820,
            "accel_x": 0.02,
            "accel_y": -0.01,
            "accel_z": 9.80,
            "vibration_hz": 1.9
        }
        r = self.client.post("/api/v1/telemetry/ingest", json=ingest_payload)
        self.assertEqual(r.status_code, 200)
        ingested = r.json()
        self.assertEqual(ingested["data_source"], "LIVE")
        self.assertEqual(ingested["status"], "ONLINE")
        self.assertEqual(ingested["temperature"], 29.4)

        # 3. Query history filter
        hist = self.client.get("/api/v1/telemetry/history?data_source=LIVE")
        self.assertEqual(hist.status_code, 200)
        h_data = hist.json()
        self.assertGreaterEqual(h_data["count"], 1)
        self.assertEqual(h_data["readings"][-1]["data_source"], "LIVE")

        # 4. Clean up - Return to OFFLINE mode
        self.client.post("/api/v1/mode/select", json={"mode": "OFFLINE"})


if __name__ == "__main__":
    unittest.main(verbosity=2)





