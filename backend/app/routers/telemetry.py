"""
Telemetry Ingestion Router for ESP32-S3 Nodes & Simulation
"""

from fastapi import APIRouter
from app.schemas.disaster import SensorReadingSchema
from app.services.sensor_trust_engine import sensor_trust_engine
from app.services.disaster_fusion_engine import disaster_fusion_engine
from app.services.communication_manager import communication_manager
from app.core.database import get_db_connection

router = APIRouter(prefix="/api/v1/telemetry", tags=["Telemetry Ingestion"])

@router.post("/ingest")
def ingest_telemetry_packet(reading: SensorReadingSchema):
    # 1. Evaluate Sensor Trust
    trust_result = sensor_trust_engine.evaluate_node(
        reading.node_id,
        reading.water_level_m,
        reading.rate_of_rise_m_min,
        [2.41, 2.42] # Baseline neighbor readings
    )

    # 2. Persist in local SQLite WAL
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telemetry (node_id, timestamp_ms, water_level_m, rate_of_rise_m_min, baro_pressure_hpa, battery_pct, safety_state, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (reading.node_id, reading.timestamp_ms, reading.water_level_m, reading.rate_of_rise_m_min, reading.baro_pressure_hpa, reading.battery_pct, reading.safety_state, reading.confidence))
    conn.commit()
    conn.close()

    # 3. Route through Communication Resilience Manager
    route_res = communication_manager.route_telemetry(reading.dict())

    return {
        "status": "PROCESSED",
        "node_id": reading.node_id,
        "trust_score": trust_result.trust_score,
        "node_status": trust_result.status,
        "communication_routing": route_res
    }
