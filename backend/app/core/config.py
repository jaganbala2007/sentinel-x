"""
Sentinel-X Backend Configuration
=================================
Centralized environment-based configuration using Pydantic Settings.
All environment variables are loaded from a .env file or system environment.

Usage:
    from app.core.config import settings
    print(settings.DATABASE_URL)
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Priority order (highest to lowest):
      1. Actual environment variables
      2. .env file values
      3. Default values defined here
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Application ---
    APP_NAME: str = "Sentinel-X Core API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # "development" | "staging" | "production"

    # --- Network ---
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://localhost:8080",
        "https://jaganbala2007.github.io",
    ]

    # --- Database ---
    DATABASE_URL: str = "postgresql://sentinel:sentinel@localhost:5432/sentinelx"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL_SECONDS: int = 30  # Telemetry cache TTL

    # --- MQTT Broker ---
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_TOPIC_TELEMETRY: str = "sentinel/telemetry/#"
    MQTT_TOPIC_ALERTS: str = "sentinel/alerts/#"

    # --- AI / Fog Configuration ---
    FOG_NODE_HOST: str = "192.168.1.100"
    FOG_NODE_PORT: int = 9000
    YOLO_MODEL_PATH: str = "models/yolov11s-ppe.onnx"
    RISK_MODEL_PATH: str = "models/risk_field_v3.pb"

    # --- PLC / Machine Control ---
    PLC_HOST: str = "192.168.1.200"
    PLC_PORT: int = 502  # Modbus TCP standard port
    PLC_UNIT_ID: int = 1

    # --- Security ---
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_USE_STRONG_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours


# Singleton settings instance — import this throughout the application
settings = Settings()
