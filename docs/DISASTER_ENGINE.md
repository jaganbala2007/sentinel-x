# Sentinel-X Disaster Fusion Engine

**Subsystem:** Core Decision-Making & Risk Assessment  
**Class:** Deterministic Additive Bayesian Evidence Model  

---

## 1. Why Not a Black-Box Neural Network for Life Safety?

Critical disaster alerts trigger physical sirens and mass evacuations. Using an opaque end-to-end deep learning or generative LLM model introduces:
1. **Hallucination Risk:** False alarms erode public trust.
2. **Unexplainable Outputs:** Emergency commanders cannot interrogate *why* the model escalated risk.
3. **Execution Latency & Dependency:** Heavy models require GPU acceleration and cloud servers.

Sentinel-X enforces **deterministic, explainable physics-grounded logic**.

---

## 2. Evidence Factor Breakdown

| Factor | Parameter | Weight (Max Pts) | Physical Basis |
| :--- | :--- | :---: | :--- |
| **Water Level ($W_{\text{stage}}$)** | Baseline exceedance | 35 | Direct measurement of river crest relative to embankments |
| **Rate of Rise ($W_{\text{rise}}$)** | $\Delta h / \Delta t$ velocity | 25 | Kinematic wave surge velocity |
| **Basin Precipitation ($W_{\text{rain}}$)**| Rain intensity (mm/h) | 14 | Catchment runoff loading |
| **Soil Saturation ($W_{\text{soil}}$)** | TDR Moisture % | 8 | Infiltration capacity deficit |
| **Spatial Consensus ($W_{\text{consensus}}$)**| Multi-node agreement | 10 | Independent physical corroboration |
| **Historical Fit ($W_{\text{hist}}$)** | Seasonal hydrograph | 2 | Historical basin response pattern |
| **Total Composite Risk** | Sum of factors | **100** | Scaled to 0–100% with severity thresholds |
