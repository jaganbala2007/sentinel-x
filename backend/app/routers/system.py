"""
Global System Status & Architecture Metadata Router
"""

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/api/v1/system", tags=["System Diagnostics"])

@router.get("/status")
def get_system_status():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "architecture": "ESP32-S3 Sensing &bull; Raspberry Pi 5 Edge &bull; HF Packet (7.105 MHz) &bull; PQC",
        "tagline": "When infrastructure fails, safety shouldn't.",
        "status": "OPERATIONAL",
        "edge_gateway": "RPI5-EDGE-01 (ONLINE)",
        "sensor_nodes_count": 20,
        "sqlite_wal": "ACTIVE",
        "pqc_status": "PROTOTYPE (ML-KEM-768 / ML-DSA-65)"
    }
