"""
Sentinel-X Explainable Disaster Risk Engine
============================================
Calculates quantitative hazard risk scores based on multi-sensor telemetry,
environmental trends, zone vulnerability, and sensor confidence metrics.

Formula:
  Risk Score = min(100, Hazard Severity x Exposure x Vulnerability x Confidence + Rate-of-Change Bonus)

Provides transparent factor attribution breakdown for EOC Decision Support.
"""

from typing import Dict, Any, List

class DisasterRiskEngine:
    def __init__(self):
        # Default weights & thresholds
        self.gas_baseline = 400.0  # MQ-135 nominal ADC baseline
        self.temp_baseline = 25.0  # Celsius nominal baseline
        self.vib_baseline = 0.5    # mm/s nominal baseline

    def calculate_risk(self, telemetry: Dict[str, Any], zone_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Computes explainable risk score (0-100) and risk level (NORMAL, WATCH, WARNING, CRITICAL)
        with factor breakdown.
        """
        gas = float(telemetry.get("gas", 400))
        temp = float(telemetry.get("temperature", 25.0))
        vib = float(telemetry.get("vibration", 0.5))
        humidity = float(telemetry.get("humidity", 50.0))
        water = float(telemetry.get("water_level_m", 0.0))
        
        trust_score = float(telemetry.get("trustScore", 100)) / 100.0
        
        # 1. Hazard Factor Calculation
        gas_contrib = 0.0
        if gas > 2500:
            gas_contrib = 35.0
        elif gas > 1500:
            gas_contrib = 20.0
        elif gas > 800:
            gas_contrib = 10.0

        temp_contrib = 0.0
        if temp >= 50.0:
            temp_contrib = 30.0
        elif temp >= 38.0:
            temp_contrib = 20.0
        elif temp >= 32.0:
            temp_contrib = 8.0

        vib_contrib = 0.0
        if vib >= 6.0:
            vib_contrib = 30.0
        elif vib >= 3.0:
            vib_contrib = 18.0
        elif vib >= 1.5:
            vib_contrib = 8.0

        water_contrib = 0.0
        if water >= 2.0:
            water_contrib = 30.0
        elif water >= 1.0:
            water_contrib = 18.0
        elif water >= 0.5:
            water_contrib = 8.0

        # Rate of change bonus
        rate_of_change_contrib = 0.0
        if telemetry.get("rate_of_rise_m_min", 0.0) > 0.1 or (gas > 2000 and temp > 40):
            rate_of_change_contrib = 10.0

        # Historical baseline factor
        historical_contrib = 5.0 if zone_info and zone_info.get("incident_count", 0) > 3 else 0.0

        # Raw Score Aggregation
        raw_score = (gas_contrib + temp_contrib + vib_contrib + water_contrib + rate_of_change_contrib + historical_contrib)
        
        # Apply Trust/Confidence multiplier
        final_score = int(round(min(100.0, raw_score * (0.5 + 0.5 * trust_score))))

        # Determine Risk Level
        if final_score >= 80:
            risk_level = "CRITICAL"
        elif final_score >= 55:
            risk_level = "WARNING"
        elif final_score >= 30:
            risk_level = "WATCH"
        else:
            risk_level = "NORMAL"

        contributors = []
        if gas_contrib > 0:
            contributors.append({"factor": "Air Quality (MQ-135)", "weight": int(gas_contrib), "value": f"{int(gas)} ADC"})
        if temp_contrib > 0:
            contributors.append({"factor": "Temperature Thermal Load", "weight": int(temp_contrib), "value": f"{temp:.1f}°C"})
        if vib_contrib > 0:
            contributors.append({"factor": "Structural Vibration", "weight": int(vib_contrib), "value": f"{vib:.2f} mm/s"})
        if water_contrib > 0:
            contributors.append({"factor": "Water Inundation Level", "weight": int(water_contrib), "value": f"{water:.2f} m"})
        if rate_of_change_contrib > 0:
            contributors.append({"factor": "Rapid Rate of Change", "weight": int(rate_of_change_contrib), "value": "Accelerating"})
        if historical_contrib > 0:
            contributors.append({"factor": "Vulnerable Zone History", "weight": int(historical_contrib), "value": "High Risk Zone"})

        if not contributors:
            contributors.append({"factor": "Baseline Environmental Stability", "weight": 0, "value": "Nominal"})

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "confidence": int(trust_score * 100),
            "contributors": contributors,
            "equation": f"Risk Score ({final_score}) = Severity ({int(raw_score)}) × Confidence ({int(trust_score * 100)}%)"
        }

risk_engine = DisasterRiskEngine()
