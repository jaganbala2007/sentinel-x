"""
Sentinel-X Storage Layer: SQLite WAL Database
=============================================
Thread-safe local database with Write-Ahead Logging (WAL) enabled.
Designed for high-throughput edge logging on Raspberry Pi 5 / USB pendrive storage.
"""

import os
import sqlite3
import threading
import json
import time
from typing import Dict, Any, List, Optional, Tuple

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(_PROJECT_ROOT, "storage", "sentinel_edge.db")

_lock = threading.Lock()

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns an open SQLite connection with WAL mode enabled."""
    path = db_path or DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, timeout=10.0, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

def init_storage_db(db_path: Optional[str] = None):
    """Initializes all schema tables if not present."""
    with _lock:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        # 1. Telemetry table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                parameter TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                timestamp REAL NOT NULL,
                data_source TEXT NOT NULL,
                trust_score REAL NOT NULL,
                trust_status TEXT NOT NULL
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_ts ON telemetry_records(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_sensor ON telemetry_records(sensor_id);")

        # 2. Incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incident_records (
                incident_id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                environment TEXT NOT NULL,
                hazard_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                risk_score REAL NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL,
                mitigation_actions TEXT
            );
        """)

        # 3. Resilient Offline Event Queue (Store-and-forward)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offline_events (
                event_id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                source TEXT NOT NULL,
                environment TEXT NOT NULL,
                hazard TEXT NOT NULL,
                risk_score REAL NOT NULL,
                priority TEXT NOT NULL,
                payload TEXT,
                sequence_num INTEGER NOT NULL,
                status TEXT NOT NULL
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_offline_status ON offline_events(status);")

        conn.commit()
        conn.close()

def execute_query(query: str, params: Tuple = (), db_path: Optional[str] = None) -> int:
    with _lock:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        row_count = cursor.rowcount
        conn.close()
        return row_count

def fetch_all(query: str, params: Tuple = (), db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def fetch_one(query: str, params: Tuple = (), db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# Initialize on module import
init_storage_db()
