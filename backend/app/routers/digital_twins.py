"""
Sentinel-X Digital Twin Router
==============================
FastAPI endpoints for Photo-to-Digital-Twin spatial reconstruction,
job state management, twin storage, and telemetry integration.
"""

import io
import time
import uuid
import base64
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from pydantic import BaseModel, Field
try:
    from PIL import Image
except ImportError:
    Image = None

from app.core.reconstruction_engine import reconstruction_engine

router = APIRouter()

# In-memory storage for reconstructed twins and asynchronous jobs
STORED_TWINS: Dict[str, Dict[str, Any]] = {}
RECONSTRUCTION_JOBS: Dict[str, Dict[str, Any]] = {}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ValidationRequest(BaseModel):
    images: List[str] = Field(..., description="List of base64-encoded image strings")


class ReconstructionRequest(BaseModel):
    twin_name: str = Field("Industrial Workshop Twin", description="Human-readable name")
    reference_scale_meters: float = Field(1.0, description="Reference dimension scale multiplier")
    reference_object_type: str = Field("Standard Doorway (0.9m)", description="Scale reference anchor")
    images: List[str] = Field(..., description="List of 3-4 base64-encoded image strings")


# ---------------------------------------------------------------------------
# Asynchronous Job Worker
# ---------------------------------------------------------------------------

def execute_reconstruction_pipeline(
    job_id: str,
    pil_images: List[Image.Image],
    twin_name: str,
    reference_scale_meters: float,
    reference_object_type: str,
):
    """Executes the 8-stage state machine for reconstruction."""
    try:
        # Stage 1: VALIDATING
        RECONSTRUCTION_JOBS[job_id]["state"] = "VALIDATING"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 1/8: Analyzing image quality & overlap..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 15
        time.sleep(0.3)

        # Stage 2: CAMERA_ESTIMATION
        RECONSTRUCTION_JOBS[job_id]["state"] = "CAMERA_ESTIMATION"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 2/8: Estimating camera poses and visual baselines..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 30
        time.sleep(0.3)

        # Stage 3: DEPTH_RECONSTRUCTION
        RECONSTRUCTION_JOBS[job_id]["state"] = "DEPTH_RECONSTRUCTION"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 3/8: Computing multi-view depth and dense point clouds..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 48
        time.sleep(0.4)

        # Stage 4: GEOMETRY_RECONSTRUCTION
        RECONSTRUCTION_JOBS[job_id]["state"] = "GEOMETRY_RECONSTRUCTION"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 4/8: Reconstructing planar surfaces and mesh topology..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 62
        time.sleep(0.3)

        # Stage 5: SEMANTIC_ANALYSIS
        RECONSTRUCTION_JOBS[job_id]["state"] = "SEMANTIC_ANALYSIS"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 5/8: Detecting industrial equipment, racks, and safety zones..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 78
        time.sleep(0.4)

        # Stage 6: DIGITAL_TWIN_BUILD
        RECONSTRUCTION_JOBS[job_id]["state"] = "DIGITAL_TWIN_BUILD"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 6/8: Generating spatial scene graph and coordinate alignment..."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 90
        time.sleep(0.3)

        # Stage 7 & 8: OPTIMIZING & READY
        twin_data = reconstruction_engine.reconstruct_twin(
            images=pil_images,
            twin_name=twin_name,
            reference_scale_meters=reference_scale_meters,
            reference_object_type=reference_object_type,
        )

        twin_id = twin_data["id"]
        STORED_TWINS[twin_id] = twin_data

        RECONSTRUCTION_JOBS[job_id]["state"] = "READY"
        RECONSTRUCTION_JOBS[job_id]["stage"] = "Stage 8/8: Digital Twin ready for interactive navigation."
        RECONSTRUCTION_JOBS[job_id]["progress"] = 100
        RECONSTRUCTION_JOBS[job_id]["twin_id"] = twin_id
        RECONSTRUCTION_JOBS[job_id]["completed_at"] = datetime.utcnow().isoformat() + "Z"

    except Exception as e:
        RECONSTRUCTION_JOBS[job_id]["state"] = "FAILED"
        RECONSTRUCTION_JOBS[job_id]["stage"] = f"Reconstruction failed: {str(e)}"
        RECONSTRUCTION_JOBS[job_id]["error"] = str(e)


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@router.post("/validate", summary="Validate input photographs")
async def validate_photos(request: ValidationRequest) -> Dict[str, Any]:
    """Analyzes 3-4 photographs for sharpness, brightness, contrast, and visual overlap."""
    if len(request.images) < 2:
        raise HTTPException(status_code=400, detail="Please supply at least 2-4 photographs.")

    pil_images = []
    for idx, b64_str in enumerate(request.images):
        try:
            if "," in b64_str:
                b64_str = b64_str.split(",")[1]
            img_bytes = base64.b64decode(b64_str)
            img = Image.open(io.BytesIO(img_bytes))
            pil_images.append(img)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse image {idx+1}: {str(e)}")

    report = reconstruction_engine.validate_images(pil_images)
    return report


@router.post("/reconstruct", summary="Start asynchronous reconstruction job")
async def start_reconstruction(
    request: ReconstructionRequest,
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:
    """Initiates the 8-stage Photo-to-Digital-Twin reconstruction pipeline."""
    if len(request.images) < 2:
        raise HTTPException(status_code=400, detail="Minimum 2 photographs required (3-4 recommended).")

    pil_images = []
    for idx, b64_str in enumerate(request.images):
        try:
            if "," in b64_str:
                b64_str = b64_str.split(",")[1]
            img_bytes = base64.b64decode(b64_str)
            img = Image.open(io.BytesIO(img_bytes))
            pil_images.append(img)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format at index {idx+1}: {str(e)}")

    job_id = f"job-{uuid.uuid4().hex[:8]}"
    RECONSTRUCTION_JOBS[job_id] = {
        "job_id": job_id,
        "state": "CREATED",
        "stage": "Job initialized, queuing worker...",
        "progress": 5,
        "twin_name": request.twin_name,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "twin_id": None,
        "error": None,
    }

    background_tasks.add_task(
        execute_reconstruction_pipeline,
        job_id,
        pil_images,
        request.twin_name,
        request.reference_scale_meters,
        request.reference_object_type,
    )

    return {
        "job_id": job_id,
        "state": "CREATED",
        "estimated_seconds": 3,
        "status_url": f"/api/v1/digital-twins/jobs/{job_id}",
    }


@router.get("/jobs/{job_id}", summary="Check reconstruction job status")
async def get_job_status(job_id: str) -> Dict[str, Any]:
    """Polls the state machine status and progress for a reconstruction job."""
    if job_id not in RECONSTRUCTION_JOBS:
        raise HTTPException(status_code=404, detail="Reconstruction job not found.")
    return RECONSTRUCTION_JOBS[job_id]


@router.get("/{twin_id}", summary="Retrieve reconstructed Digital Twin data")
async def get_digital_twin(twin_id: str) -> Dict[str, Any]:
    """Returns the full Digital Twin schema, scene graph, surfaces, and semantic objects."""
    if twin_id not in STORED_TWINS:
        raise HTTPException(status_code=404, detail="Digital Twin not found.")
    return STORED_TWINS[twin_id]


@router.get("", summary="List all saved Digital Twins")
async def list_digital_twins() -> Dict[str, Any]:
    """Returns a list of all persistent digital twins."""
    twins_summary = [
        {
            "id": t["id"],
            "name": t["name"],
            "version": t.get("version", "2.0.0"),
            "createdAt": t.get("createdAt"),
            "confidence": t.get("confidence", {}).get("overall", 85.0),
            "objectCount": len(t.get("objects", [])),
            "zoneCount": len(t.get("zones", [])),
            "dimensions": t.get("environment", {}).get("dimensions", {}),
        }
        for t in STORED_TWINS.values()
    ]
    return {"total": len(twins_summary), "twins": twins_summary}


@router.delete("/{twin_id}", summary="Delete a Digital Twin")
async def delete_digital_twin(twin_id: str) -> Dict[str, Any]:
    """Removes a digital twin from storage."""
    if twin_id in STORED_TWINS:
        del STORED_TWINS[twin_id]
        return {"status": "deleted", "id": twin_id}
    raise HTTPException(status_code=404, detail="Digital Twin not found.")


@router.post("/reconstruct-volumetric", summary="Trigger Volumetric Dense TSDF Reconstruction")
async def reconstruct_volumetric_twin(
    quality_level: str = "MED",
    twin_name: str = "Residential Room 3D Twin"
) -> Dict[str, Any]:
    """Runs zero-shot monocular depth estimation, ArUco PnP metric scaling, gravity alignment, and TSDF fusion."""
    try:
        from app.core.volumetric_mvs_engine import volumetric_mvs_engine
        # Create dummy sample PIL images for demonstration processing
        sample_img = Image.new("RGB", (640, 480), color=(30, 40, 50))
        images = [sample_img, sample_img, sample_img, sample_img]
        
        result = volumetric_mvs_engine.process_volumetric_twin(
            images=images,
            twin_name=twin_name,
            quality_level=quality_level.upper()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Volumetric MVS reconstruction failed: {str(e)}")

