# Sentinel-X Datasets

## Overview

This directory documents the datasets used to train Sentinel-X AI models. Raw dataset files are **not included** in this repository due to size. Download links and preparation scripts are provided below.

---

## Dataset Registry

### 1. PPE Detection Dataset

| Property | Value |
|---|---|
| **Purpose** | Train YOLOv11s-PPE model for helmet, vest, gloves detection |
| **Total Images** | 45,000 |
| **Train/Val/Test Split** | 80% / 10% / 10% |
| **Annotation Format** | YOLO txt (class cx cy w h) |
| **Classes** | `helmet`, `no_helmet`, `vest`, `no_vest`, `gloves`, `no_gloves` |
| **Source** | RoboFlow Construction Safety universe + proprietary industrial data |
| **License** | CC BY 4.0 |

**Download:**
```bash
pip install roboflow
python datasets/scripts/download_ppe_dataset.py
```

**Class Distribution:**
```
helmet      : 18,420 instances
no_helmet   :  6,230 instances
vest        : 17,800 instances
no_vest     :  5,940 instances
gloves      : 12,100 instances
no_gloves   :  4,510 instances
```

---

### 2. Fall Detection Dataset

| Property | Value |
|---|---|
| **Purpose** | Train pose estimation fall classifier |
| **Total Clips** | 12,000 video sequences |
| **Fall Events** | 4,200 labeled fall scenarios |
| **Normal Events** | 7,800 labeled normal behavior sequences |
| **Frame Rate** | 30fps |
| **Resolution** | 1280×720 |
| **Source** | Le2i Fall Detection + proprietary industrial footage |

---

### 3. Industrial Gas Sensor Calibration Data

| Property | Value |
|---|---|
| **Purpose** | Anomaly threshold calibration for CO2, H2S, LEL sensors |
| **Readings** | 2.8 million time-series readings |
| **Duration** | 18 months continuous monitoring |
| **Sensors** | 128 gas sensors across 4 factory zones |
| **Format** | Parquet (time-partitioned) |

---

### 4. Worker Fatigue Study Data (Digital DNA)

| Property | Value |
|---|---|
| **Purpose** | Train Digital DNA Fatigue Coefficient™ model |
| **Participants** | 340 industrial workers |
| **Duration** | 18-month longitudinal study |
| **Features** | HRV, SpO2, time-on-floor, movement entropy, incident proximity |
| **Labels** | Expert-validated fatigue ratings (1–10 scale) |
| **Ethics** | IRB approved, anonymized, GDPR compliant |

---

## Dataset Directory Structure

```
datasets/
├── ppe/
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── labels/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── dataset.yaml
├── fall_detection/
│   ├── clips/
│   └── annotations.csv
├── gas_calibration/
│   └── readings_2025.parquet
└── fatigue_study/
    └── anonymized_vitals.csv
```

---

## Data Preparation Scripts

```bash
# Download and prepare PPE dataset
python datasets/scripts/download_ppe_dataset.py

# Validate dataset integrity
python datasets/scripts/validate_dataset.py --dataset ppe

# Generate train/val/test splits
python datasets/scripts/split_dataset.py --ratio 0.8 0.1 0.1
```

---

## Data Privacy & Ethics

- All worker biometric data in the fatigue study is **fully anonymized**
- No personally identifiable information (PII) is stored in model training data
- GDPR Article 9 (special category biometric data) compliance ensured
- Dataset access requires signing a data use agreement (DUA)
- Production deployments must obtain explicit worker consent per local labor law
