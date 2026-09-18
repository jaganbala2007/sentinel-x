"""
Sentinel-X Core Compatibility Package
======================================
Re-exports ALL top-level core package components so that legacy
``from app.core.X import Y`` imports continue to work without change.
"""
import sys
import os

_root = os.path.dirname(  # repo root
    os.path.dirname(      # backend/
    os.path.dirname(      # backend/app/
    os.path.dirname(      # backend/app/core/
    os.path.abspath(__file__)))))
if _root not in sys.path:
    sys.path.insert(0, _root)

# ── Foundational ──────────────────────────────────────────────────────────────
from core.config import settings, Settings                            # noqa: F401
from core.database import (                                           # noqa: F401
    get_db_connection, init_db,
)

# ── Safety & Trust ────────────────────────────────────────────────────────────
from core.trust_engine import (                                       # noqa: F401
    TrustEngine, trust_engine, SensorObservation, DataProvenance,
)
from core.worker_safety import worker_safety_engine                   # noqa: F401
from core.machine_safety import machine_safety_engine                 # noqa: F401
from core.environment_safety import environment_safety_engine         # noqa: F401

# ── Risk & Decision ───────────────────────────────────────────────────────────
from core.risk_engine import unified_risk_engine                      # noqa: F401
from core.decision_engine import safety_decision_engine               # noqa: F401
from core.rul_engine import rul_engine                                # noqa: F401

# ── Intelligence ──────────────────────────────────────────────────────────────
from core.anomaly_engine import anomaly_engine                        # noqa: F401
from core.fusion_engine import fusion_engine                          # noqa: F401
from core.incident_engine import incident_reconstruction_engine       # noqa: F401
from core.event_engine import event_engine                            # noqa: F401
from core.response_engine import response_engine                      # noqa: F401
from core.what_if_engine import what_if_engine, WhatIfRequest         # noqa: F401
from core.copilot_engine import industrial_ai_copilot                 # noqa: F401
from core.cyber_integrity_engine import cyber_integrity_engine        # noqa: F401

# ── Reconstruction & Telemetry ────────────────────────────────────────────────
from core.reconstruction_engine import reconstruction_engine          # noqa: F401
from core.telemetry_provider import telemetry_manager as telemetry_provider  # noqa: F401
from core.sensor_abstraction import sensor_registry as sensor_abstraction_layer  # noqa: F401
from core.dataset_trainer import vision_dataset_trainer               # noqa: F401
