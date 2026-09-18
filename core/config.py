"""
Sentinel-X Disaster Intelligence & Edge Resilience Configuration
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel-X Disaster Intelligence & Emergency Command"
    VERSION: str = "2.4.1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # Hydraulic & Disaster Thresholds
    DISASTER_WATER_WARNING_LEVEL: float = 3.00   # Meters
    DISASTER_WATER_CRITICAL_LEVEL: float = 3.50  # Meters
    RATE_OF_RISE_WARNING: float = 0.04           # m/min
    RATE_OF_RISE_CRITICAL: float = 0.08          # m/min
    
    # Sensor Trust & Byzantine Quarantine
    SENSOR_TRUST_THRESHOLD: float = 50.0         # Below 50% = QUARANTINE
    CONSENSUS_TOLERANCE_M: float = 0.35          # Tolerance between adjacent nodes
    
    # Communication Resilience
    DEFAULT_COMM_MODE: str = "NORMAL"            # NORMAL, DEGRADED, EMERGENCY, ISOLATED
    HF_FREQUENCY_MHZ: float = 7.105              # 40m Band Amateur Radio Emergency Frequency
    HF_BAUD_RATE: int = 1200                     # 1200 Baud AFSK AX.25
    
    # Offline Persistence
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "sentinel_edge.db")
    OFFLINE_QUEUE_LIMIT: int = 5000
    
    # Security
    PQC_ALGORITHM_KEM: str = "ML-KEM-768"
    PQC_ALGORITHM_SIG: str = "ML-DSA-65"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()
