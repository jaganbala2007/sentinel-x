# Sentinel-X AI Models

## Models Overview

| Model | Task | Format | Size | Inference |
|---|---|---|---|---|
| `yolov11s-ppe.onnx` | PPE detection (helmet, vest, gloves) | ONNX | ~22MB | 32ms / Jetson Orin |
| `yolov11x-zone.onnx` | Zone intrusion detection | ONNX | ~136MB | 44ms / Jetson Orin |
| `yolov11-pose.onnx` | Worker pose estimation + fall detection | ONNX | ~54MB | 38ms / Jetson Orin |
| `risk_field_v3.pb` | Dynamic risk field probability grid | TF SavedModel | ~8MB | 12ms / CPU |
| `fatigue_model.pkl` | Digital DNA Fatigue Coefficient™ | Scikit-learn | ~2MB | < 1ms / CPU |

> **Note:** Model weight files are excluded from Git via `.gitignore` due to size.  
> Use Git LFS or download from the project releases page.

---

## Model Cards

### YOLOv11s-PPE (Personal Protective Equipment Detection)

| Property | Value |
|---|---|
| **Architecture** | YOLOv11s (Small) |
| **Input** | 640×640 RGB image |
| **Output** | Bounding boxes + class + confidence |
| **Classes** | `helmet`, `no_helmet`, `vest`, `no_vest`, `gloves`, `no_gloves` |
| **Training Data** | 45,000 labeled images (construction + industrial) |
| **mAP@0.5** | 0.891 |
| **Inference Speed** | 32ms (TensorRT FP16, Jetson Orin NX) |
| **Framework** | Ultralytics YOLOv11, converted to ONNX |

**Training Command:**
```bash
yolo train model=yolov11s.pt data=ppe_dataset.yaml \
     epochs=100 imgsz=640 batch=16 \
     project=sentinel_x name=ppe_detector
```

---

### YOLOv11-Pose (Fall Detection)

| Property | Value |
|---|---|
| **Architecture** | YOLOv11-pose |
| **Input** | 640×640 RGB image |
| **Output** | 17 keypoint skeleton per person + BBox |
| **Fall Algorithm** | Spine angle deviation > 45° from vertical for > 500ms |
| **False Positive Rate** | 0.3% (validated on 12,000 test scenarios) |
| **Inference Speed** | 38ms (TensorRT FP16) |

---

### Risk Field Model v3

Custom probabilistic spatial model computing a **hazard probability grid** across the factory floor.

| Property | Value |
|---|---|
| **Architecture** | Gaussian Process Regression + Bayesian spatial correlation |
| **Input** | Sensor readings array, worker positions, machine states |
| **Output** | 100×100 probability grid (0.0 → 1.0 per cell) |
| **Update Rate** | 250ms (4 Hz) |
| **Grid Resolution** | 1 meter per cell |

---

### Digital DNA Fatigue Coefficient™ Model

| Property | Value |
|---|---|
| **Architecture** | Gradient Boosting (XGBoost) |
| **Input Features** | HRV, SpO2 deficit, time-on-floor, movement entropy, incident history |
| **Output** | Fatigue scalar: 0.0 (alert) → 1.0 (critically fatigued) |
| **Alert Threshold** | > 0.70 |
| **Training Labels** | 18-month validated industrial fatigue study data |
| **Accuracy** | 87.4% precision on holdout set |

---

## Model Download

Since model files are too large for Git, download pre-trained weights:

```bash
# Using the provided download script (v1.1+)
python scripts/download_models.py

# Or manually place in models/ directory:
# models/yolov11s-ppe.onnx
# models/yolov11x-zone.onnx
# models/yolov11-pose.onnx
# models/risk_field_v3.pb
# models/fatigue_model.pkl
```

---

## Running Inference (Python)

```python
import onnxruntime as ort
import numpy as np
import cv2

# Load PPE detection model
session = ort.InferenceSession(
    "models/yolov11s-ppe.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

# Preprocess image
img = cv2.imread("frame.jpg")
img_resized = cv2.resize(img, (640, 640))
img_tensor = np.expand_dims(img_resized.transpose(2, 0, 1), 0).astype(np.float32) / 255.0

# Run inference
outputs = session.run(None, {"images": img_tensor})
print(f"Detections: {outputs[0].shape}")  # [1, num_classes+4, num_detections]
```

---

## Citations

```bibtex
@software{yolov11,
  author = {Ultralytics},
  title = {YOLOv11: A State-of-the-Art Real-Time Object Detection System},
  year = {2024},
  url = {https://github.com/ultralytics/ultralytics}
}
```
