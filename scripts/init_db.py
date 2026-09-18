"""
Sentinel-X CLI Utility: Initialize Database
===========================================
Creates SQLite WAL tables in the storage directory.
"""
import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from storage.database import init_storage_db, DEFAULT_DB_PATH

if __name__ == "__main__":
    print(f"Initializing Sentinel-X Storage Database at: {DEFAULT_DB_PATH}")
    init_storage_db()
    print("Database initialized successfully with WAL journal mode.")
