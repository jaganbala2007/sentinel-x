"""
Backend export shim for volumetric_mvs_engine.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from core.volumetric_mvs_engine import (
    VolumetricMVSEngine,
    DepthEstimator,
    ArucoPnPScaleRectifier,
    GravityNorthAligner,
    VolumetricTSDFFusion,
    WeightedTextureBaker,
    SimStatusEvaluator,
    volumetric_mvs_engine,
)

__all__ = [
    "VolumetricMVSEngine",
    "DepthEstimator",
    "ArucoPnPScaleRectifier",
    "GravityNorthAligner",
    "VolumetricTSDFFusion",
    "WeightedTextureBaker",
    "SimStatusEvaluator",
    "volumetric_mvs_engine",
]
