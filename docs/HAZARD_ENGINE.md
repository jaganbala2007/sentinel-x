# Sentinel-X V2 — Pluggable Hazard Engine Specification

## 1. Architectural Philosophy

The Sentinel-X Hazard Engine enforces strict **separation of concerns**:
$$\text{Sensor Telemetry} \xrightarrow{\text{Verification}} \text{Sensor Trust} \xrightarrow{\text{Isolation}} \text{Hazard Modules} \xrightarrow{\text{Synthesis}} \text{Risk Engine} \xrightarrow{\text{Policy}} \text{Response}$$

- **No Single Sensor Can Trigger a Critical Alert Alone**: Hazard modules require cross-sensor or multi-node correlation to prevent false evacuations caused by transient sensor faults.
- **Byzantine Quarantined Nodes Are Automatically Stripped**: Only nodes with $\text{Trust Score} \ge 50.0$ are admitted into hazard calculations.
- **Explainable Evidence Chains**: Every hazard evaluation outputs an evidentiary log explaining why a threshold was reached and which sensors contributed.

---

## 2. Mathematical Formulations by Hazard Module

### 1. Flood & Flash-Flood Module (`FloodHazardModule`) — *SIH Hero Module*
Inputs: Verified water level $h$ (m), kinematic rate of rise $\Delta h / \Delta t$ (m/min), barometric pressure $P$ (hPa), and rainfall intensity $R$ (mm/hr).

$$\text{Risk}_{\text{flood}} = \text{Base} + f(h) + g\left(\frac{\Delta h}{\Delta t}\right) + \text{ConsensusBonus}$$

- If $h \ge 3.50$ m or $h_{\max} \ge 3.80$ m: $+50$ points.
- If $h \ge 3.10$ m: $+30$ points.
- If $\frac{\Delta h}{\Delta t} \ge 0.08$ m/min: $+25$ points.
- Multi-Node Consensus: Confidence $C = \min(98, 70 + 8 \cdot N_{\text{trusted}})$.

### 2. Fire & Thermal Smoke Module (`FireHazardModule`)
Inputs: Ambient temperature $T$ (°C), rate of temperature rise $\Delta T / \Delta t$, optical smoke particulate obscuration $S$ (%/m), and carbon monoxide concentration $\text{CO}$ (ppm).

$$\text{Risk}_{\text{fire}} = \text{Base} + f(T) + g(S) + h(\text{CO})$$

- If $T \ge 65.0$ °C: $+45$ points.
- If $S \ge 4.0$ %/m: $+40$ points.
- Co-occurrence: If both $T \ge 45$ °C and $S \ge 1.5$ %/m occur simultaneously, confidence jumps to $92\%$, distinguishing real fires from harmless dust or cooking steam.

### 3. Gas Leak Module (`GasHazardModule`)
Inputs: Combustible or toxic gas concentration $G$ (ppm), atmospheric airflow, and manifold pressure.

$$\text{Risk}_{\text{gas}} = \begin{cases} 
5 + 75 = 80 & \text{if } G \ge 100 \text{ ppm (CRITICAL)} \\
5 + 40 = 45 & \text{if } 50 \le G < 100 \text{ ppm (WARNING)} \\
5 + 20 = 25 & \text{if } 25 \le G < 50 \text{ ppm (WATCH)} \\
5 & \text{otherwise (NORMAL)}
\end{cases}$$

- Critical action triggers automatic process valve isolation and exhaust scrubbing.

### 4. Structural Anomaly Module (`StructuralHazardModule`)
Inputs: Peak resonant vibration velocity $v_{\text{rms}}$ (mm/s), angular tilt $\theta$ (°).

$$\text{Risk}_{\text{structural}} = \text{Base} + f(v) + g(\theta)$$

- If $v \ge 7.5$ mm/s: $+50$ points.
- If $\theta \ge 2.0$°: $+35$ points.
- If both occur simultaneously: $\text{Risk} \ge 90\% \implies \text{CRITICAL}$, issuing immediate highway closure or dam gate relief orders.

### 5. Power & Grid Failure Module (`PowerHazardModule`)
Inputs: DC bus voltage $V_{\text{bus}}$ (V), battery state-of-charge $\text{SoC}$ (%).

- If $V_{\text{bus}} \le 10.5$ V or $\text{SoC} \le 15\%$: $+75$ points $\implies$ Triggers **EMERGENCY_POWER** state (sheds non-critical telemetry, halts non-essential radio broadcasts, and protects the 12V siren relay reserve).

---

## 3. Multi-Hazard Compounding Engine

When multiple hazards occur concurrently (e.g., Flash Flood + Landslide or Fire + Toxic Gas), the **Universal Risk Engine** evaluates:

$$\text{Overall Risk} = \max(\text{Risk}_{1}, \dots, \text{Risk}_{k}) + \min\left(15, \sum_{i=2}^{k} [\text{Risk}_{i} \ge 40] \cdot 8\right)$$

This mathematical compounding ensures that cascading multi-hazard disasters are prioritized immediately without arbitrary heuristics.
