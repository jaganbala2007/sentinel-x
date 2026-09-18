"""
Sentinel-X Dashboard Server
===========================
FastAPI application serving the SCADA EOC Command Center and 3D Digital Twin Cockpit.
Can be run via:
    uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --reload
"""

import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard.app:app", host="0.0.0.0", port=8000, reload=True)
