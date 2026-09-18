# ⚠️ Sentinel-X Engineering Limitations & Operational Boundaries

**Document Version:** 2.4.0  
**Honesty Statement:** Sentinel-X is an advanced research and engineering prototype built for SIH 2026. This document explicitly defines what is physically verified vs simulated, avoiding any overclaiming during technical evaluation.

---

## 1. Explicit Subsystem Operational Boundaries

1. **Non-Certified Prototype Disclaimer:**
   - Sentinel-X is designed with architectural patterns inspired by **IEC 61508 (SIL-2)** and **ISO 13849 (Category 3)**, but is **NOT a formally certified functional safety system**. Formal TÜV certification requires third-party hardware qualification, redundant power supplies, and silicon-level fault injection testing.

2. **Communication Subsystem Status:**
   - **Internet / LAN / Wi-Fi:** `LIVE` and physically tested.
   - **HF Packet Radio (AX.25 / ALE):** `SIMULATED` in software with ionospheric noise, CRC-32 verification, and ARQ retries. Physical transmission requires external 100W HF transceivers (e.g., Icom IC-7300) and amateur/commercial radio licensing.
   - **Satellite Communications:** `ADAPTER READY` via REST endpoints configured for open-source SatNOGS ground stations.

3. **Photo-Assisted Digital Twin Scope:**
   - The photogrammetry engine extracts dominant color palettes, estimates spatial bounding boxes, segments components via DeepLabV3+, and generates watertight Poisson surface statistics.
   - It is an **assistive operational digital twin**, not sub-millimeter industrial LIDAR metrology.

4. **Quantum Cryptography Status:**
   - Cryptographic packet signing utilizes standard **Micro-ECC SECP256R1 ECDSA**. Post-Quantum Cryptography (PQC ML-KEM/Dilithium) exists as an experimental software prototype and is not claimed as certified quantum-proof defense.
