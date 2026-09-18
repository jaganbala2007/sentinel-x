"""
Sentinel-X Local Edge SQLite Persistence & Store-and-Forward WAL Engine
"""

import sqlite3
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.config import settings

logger = logging.getLogger("sentinel.database")

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable Write-Ahead Logging (WAL) for high concurrency and crash resilience
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

get_db = get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Telemetry table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT NOT NULL,
        timestamp_ms INTEGER NOT NULL,
        water_level_m REAL NOT NULL,
        rate_of_rise_m_min REAL NOT NULL,
        baro_pressure_hpa REAL,
        soil_saturation_pct REAL,
        battery_pct INTEGER,
        safety_state INTEGER,
        confidence REAL,
        raw_json TEXT
    );
    """)

    # 2. Offline Store-and-Forward Event Queue table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offline_events (
        event_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        node_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        risk_score INTEGER NOT NULL,
        confidence INTEGER NOT NULL,
        payload TEXT NOT NULL,
        sync_status TEXT DEFAULT 'PENDING',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Sensor Trust State table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_trust (
        node_id TEXT PRIMARY KEY,
        trust_score REAL NOT NULL,
        status TEXT NOT NULL,
        quarantine_reasons TEXT,
        last_evaluated DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Hazard Zones table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zones (
        zone_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'NORMAL',
        hazard_level INTEGER DEFAULT 0,
        occupancy INTEGER DEFAULT 0,
        sensor_nodes TEXT,
        last_update TEXT
    );
    """)

    # 5. Disaster Incidents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disaster_incidents (
        incident_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        zone_id TEXT NOT NULL,
        disaster_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'DETECTED',
        confidence REAL NOT NULL,
        evidence_json TEXT,
        operator TEXT,
        assigned_team TEXT,
        resolution TEXT
    );
    """)

    # 6. Evacuation Routes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evacuation_routes (
        route_id TEXT PRIMARY KEY,
        from_zone TEXT NOT NULL,
        to_exit TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'CLEAR',
        hazard_level INTEGER DEFAULT 0
    );
    """)

    # 7. Emergency Resources table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_resources (
        resource_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'AVAILABLE',
        assigned_incident_id TEXT,
        location TEXT
    );
    """)

    # 8. Immutable Audit Log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user_role TEXT NOT NULL,
        action TEXT NOT NULL,
        incident_id TEXT,
        zone_id TEXT,
        prev_state TEXT,
        new_state TEXT,
        details TEXT
    );
    """)

    # 9. Post-Disaster Recovery Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recovery_reports (
        report_id TEXT PRIMARY KEY,
        incident_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        duration_sec INTEGER NOT NULL,
        affected_zones TEXT NOT NULL,
        peak_severity TEXT NOT NULL,
        evidence_summary TEXT,
        actions_summary TEXT,
        resources_used TEXT,
        damage_assessment TEXT
    );
    """)

    conn.commit()
    conn.close()
    logger.info("Initialized local SQLite edge database at %s (WAL Enabled & Disaster Management Schemas Active)", settings.SQLITE_DB_PATH)

# Initialize on module load
init_db()

