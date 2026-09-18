"""
Sentinel-X V2 Pluggable Hazard Engine
=====================================
Modular hazard intelligence modules. Each module evaluates normalized,
trusted sensor readings to detect specific physical hazard conditions.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from app.schemas.universal import (
    NormalizedSensorReading,
    HazardAssessment,
    HazardType,
    SeverityLevel,
    EnvironmentProfile,
    EnvironmentType
)

class BaseHazardModule(ABC):
    @property
    @abstractmethod
    def hazard_type(self) -> HazardType:
        pass

    @abstractmethod
    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        """
        Evaluate normalized sensor readings from trusted nodes.
        Only readings from nodes with trust >= 50.0 should contribute to decisions.
        """
        pass

# ---------------------------------------------------------------------------
# 1. Flood Hazard Module (SIH Hero Demonstration)
# ---------------------------------------------------------------------------

class FloodHazardModule(BaseHazardModule):
    @property
    def hazard_type(self) -> HazardType:
        return HazardType.FLASH_FLOOD

    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        # Filter for water depth / level sensors from non-quarantined nodes
        water_readings = [
            r for r in readings 
            if ("water" in r.metric_name or "depth" in r.metric_name) 
            and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        
        if not water_readings:
            return None

        # Calculate average verified water level and rate of rise
        avg_level = sum(r.value for r in water_readings) / len(water_readings)
        max_level = max(r.value for r in water_readings)
        
        # Check rate of rise from auxiliary metrics if available
        rates = [r.auxiliary_metrics.get("rate_of_rise_m_min", 0.0) for r in water_readings]
        avg_rate = sum(rates) / len(rates) if rates else 0.0

        evidence = []
        # Multi-factor risk calculation
        risk = 10
        if avg_level >= 3.50 or max_level >= 3.80:
            risk += 50
            evidence.append(f"Water stage critical at {max_level:.2f}m (threshold 3.50m)")
        elif avg_level >= 3.10:
            risk += 30
            evidence.append(f"Water level rising high: {avg_level:.2f}m")
        elif avg_level >= 2.70:
            risk += 15
            evidence.append(f"Mild water level elevation: {avg_level:.2f}m")
        else:
            evidence.append(f"Water level laminar within baseline: {avg_level:.2f}m")

        if avg_rate >= 0.08:
            risk += 25
            evidence.append(f"Rapid kinematic surge rate: +{avg_rate:.2f} m/min")
        elif avg_rate >= 0.03:
            risk += 12
            evidence.append(f"Upward trend detected: +{avg_rate:.2f} m/min")

        # Consensus confidence
        trusted_count = len(water_readings)
        confidence = min(98, 70 + (trusted_count * 8))
        evidence.append(f"{trusted_count} independent sensor nodes in consensus")

        # Determine severity
        if risk >= 75:
            severity = SeverityLevel.CRITICAL
            action = "TRIGGER LOCAL SIREN RELAY & EVACUATE LOWLAND SECTORS"
        elif risk >= 50:
            severity = SeverityLevel.WARNING
            action = "DISPATCH REGIONAL FLOOD WARNING VIA HF PACKET & SATELLITE"
        elif risk >= 25:
            severity = SeverityLevel.WATCH
            action = "INCREASE SENSOR POLLING RATE & ALERT EOC"
        else:
            severity = SeverityLevel.NORMAL
            action = "CONTINUE HYDROLOGICAL MONITORING"

        return HazardAssessment(
            hazard_type=self.hazard_type,
            risk_score=min(100, risk),
            confidence=confidence,
            severity=severity,
            primary_metric="water_level_m",
            primary_value=round(max_level, 2),
            evidence=evidence,
            affected_zone="BASIN 04 / TEESTA SECTOR B",
            recommended_action=action
        )

# ---------------------------------------------------------------------------
# 2. Fire Hazard Module (Indoor / Industrial / Urban)
# ---------------------------------------------------------------------------

class FireHazardModule(BaseHazardModule):
    @property
    def hazard_type(self) -> HazardType:
        return HazardType.FIRE

    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        # Look for temperature, smoke, and CO
        temp_readings = [
            r for r in readings 
            if ("temp" in r.metric_name) and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        smoke_readings = [
            r for r in readings 
            if ("smoke" in r.metric_name) and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        
        if not temp_readings and not smoke_readings:
            return None

        max_temp = max([r.value for r in temp_readings], default=25.0)
        max_smoke = max([r.value for r in smoke_readings], default=0.0)

        risk = 5
        evidence = []

        if max_temp >= 65.0:
            risk += 45
            evidence.append(f"Extreme ambient thermal spike: {max_temp:.1f}°C")
        elif max_temp >= 45.0:
            risk += 20
            evidence.append(f"Elevated temperature: {max_temp:.1f}°C")
        else:
            evidence.append(f"Ambient temperature normal: {max_temp:.1f}°C")

        if max_smoke >= 4.0:
            risk += 40
            evidence.append(f"Dense optical smoke particulate: {max_smoke:.1f} %/m")
        elif max_smoke >= 1.5:
            risk += 20
            evidence.append(f"Smoke particulate detected: {max_smoke:.1f} %/m")

        confidence = 92 if (temp_readings and smoke_readings) else 75
        if temp_readings and smoke_readings:
            evidence.append("Thermal and particulate sensors mutually confirm hazard")

        if risk >= 70:
            severity = SeverityLevel.CRITICAL
            action = "ACTIVATE FIRE SUPPRESSION & BUILDING EVACUATION ALARM"
        elif risk >= 40:
            severity = SeverityLevel.WARNING
            action = "DISPATCH SECURITY INSPECTION & PREPARE SUPPRESSION"
        elif risk >= 20:
            severity = SeverityLevel.WATCH
            action = "MONITOR AIR DUCTS & VENTILATION"
        else:
            severity = SeverityLevel.NORMAL
            action = "ENVIRONMENT THERMALLY STABLE"

        return HazardAssessment(
            hazard_type=self.hazard_type,
            risk_score=min(100, risk),
            confidence=confidence,
            severity=severity,
            primary_metric="temperature_c",
            primary_value=round(max_temp, 1),
            evidence=evidence,
            affected_zone="FACILITY ZONE 02 / ENCLOSURE C",
            recommended_action=action
        )

# ---------------------------------------------------------------------------
# 3. Gas Leak Hazard Module (Industrial / Process / Indoor)
# ---------------------------------------------------------------------------

class GasHazardModule(BaseHazardModule):
    @property
    def hazard_type(self) -> HazardType:
        return HazardType.GAS_LEAK

    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        gas_readings = [
            r for r in readings 
            if ("gas" in r.metric_name or "co" in r.metric_name or "ch4" in r.metric_name) 
            and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        
        if not gas_readings:
            return None

        max_gas = max(r.value for r in gas_readings)
        evidence = []
        risk = 5

        if max_gas >= 100.0:
            risk += 75
            evidence.append(f"Toxic/combustible gas concentration critical: {max_gas:.1f} ppm")
        elif max_gas >= 50.0:
            risk += 40
            evidence.append(f"Gas concentration above OSHA permissible limit: {max_gas:.1f} ppm")
        elif max_gas >= 25.0:
            risk += 20
            evidence.append(f"Trace gas accumulation detected: {max_gas:.1f} ppm")
        else:
            evidence.append(f"Atmospheric gas levels clean: {max_gas:.1f} ppm")

        confidence = 94 if len(gas_readings) >= 2 else 80
        evidence.append(f"{len(gas_readings)} gas monitoring points evaluated")

        if risk >= 75:
            severity = SeverityLevel.CRITICAL
            action = "TRIGGER EMERGENCY EXHAUST VENTILATION & ISOLATE VALVES"
        elif risk >= 45:
            severity = SeverityLevel.WARNING
            action = "ACTIVATE LOCAL HAZARD STROBE & ALERT SAFETY WARDENS"
        elif risk >= 20:
            severity = SeverityLevel.WATCH
            action = "INSPECT PIPING SEALS & PRESSURE FITTINGS"
        else:
            severity = SeverityLevel.NORMAL
            action = "ATMOSPHERE NOMINAL"

        return HazardAssessment(
            hazard_type=self.hazard_type,
            risk_score=min(100, risk),
            confidence=confidence,
            severity=severity,
            primary_metric="gas_concentration_ppm",
            primary_value=round(max_gas, 1),
            evidence=evidence,
            affected_zone="PROCESS BAY 01 / MANIFOLD LINE",
            recommended_action=action
        )

# ---------------------------------------------------------------------------
# 4. Structural Anomaly Hazard Module (Infrastructure / Civil / Dam)
# ---------------------------------------------------------------------------

class StructuralHazardModule(BaseHazardModule):
    @property
    def hazard_type(self) -> HazardType:
        return HazardType.STRUCTURAL_ANOMALY

    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        vib_readings = [
            r for r in readings 
            if ("vibration" in r.metric_name or "accel" in r.metric_name) 
            and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        tilt_readings = [
            r for r in readings 
            if ("tilt" in r.metric_name or "incline" in r.metric_name) 
            and trust_map.get(r.node_id, 100.0) >= 50.0
        ]

        if not vib_readings and not tilt_readings:
            return None

        # Check primary readings and auxiliary metrics
        aux_tilts = [
            r.auxiliary_metrics["tilt_deg"] 
            for r in readings 
            if "tilt_deg" in r.auxiliary_metrics and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        primary_tilts = [r.value for r in tilt_readings]
        all_tilts = primary_tilts + aux_tilts
        max_tilt = max(all_tilts, default=0.1)
        max_vib = max([r.value for r in vib_readings], default=1.0)

        risk = 5
        evidence = []

        if max_vib >= 7.5:
            risk += 50
            evidence.append(f"Severe resonant vibration peak: {max_vib:.2f} mm/s")
        elif max_vib >= 4.0:
            risk += 25
            evidence.append(f"Elevated structural oscillation: {max_vib:.2f} mm/s")
        else:
            evidence.append(f"Vibration within static limits: {max_vib:.2f} mm/s")

        if max_tilt >= 2.0:
            risk += 35
            evidence.append(f"Significant foundation deflection: {max_tilt:.2f}°")
        elif max_tilt >= 0.8:
            risk += 15
            evidence.append(f"Mild angular tilt: {max_tilt:.2f}°")

        has_tilt = len(all_tilts) > 0
        confidence = 90 if (vib_readings and has_tilt) else 78

        if risk >= 75:
            severity = SeverityLevel.CRITICAL
            action = "IMMEDIATE STRUCTURAL CLOSURE & BEARING INSPECTION"
        elif risk >= 45:
            severity = SeverityLevel.WARNING
            action = "RESTRICT HEAVY TRAFFIC LOAD & COMMENCE NDT AUDIT"
        elif risk >= 20:
            severity = SeverityLevel.WATCH
            action = "CONTINUE HIGH-RATE ACCELEROMETER TELEMETRY"
        else:
            severity = SeverityLevel.NORMAL
            action = "STRUCTURAL INTEGRITY STABLE"

        return HazardAssessment(
            hazard_type=self.hazard_type,
            risk_score=min(100, risk),
            confidence=confidence,
            severity=severity,
            primary_metric="vibration_mm_s",
            primary_value=round(max_vib, 2),
            evidence=evidence,
            affected_zone="PIER 03 / GIRDER SPAN B",
            recommended_action=action
        )

# ---------------------------------------------------------------------------
# 5. Power & Grid Failure Hazard Module
# ---------------------------------------------------------------------------

class PowerHazardModule(BaseHazardModule):
    @property
    def hazard_type(self) -> HazardType:
        return HazardType.POWER_FAILURE

    def evaluate(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> Optional[HazardAssessment]:
        voltage_readings = [
            r for r in readings 
            if ("voltage" in r.metric_name or "bus_v" in r.metric_name) 
            and trust_map.get(r.node_id, 100.0) >= 50.0
        ]
        
        # Also check battery percentages across all readings
        batteries = [r.battery_pct for r in readings if trust_map.get(r.node_id, 100.0) >= 50.0]
        min_battery = min(batteries, default=100)
        min_v = min([r.value for r in voltage_readings], default=12.4)

        risk = 5
        evidence = []

        if min_v <= 10.5 or min_battery <= 15:
            risk += 75
            evidence.append(f"Critical battery depletion ({min_battery}%) or bus drop ({min_v:.1f}V)")
        elif min_v <= 11.4 or min_battery <= 35:
            risk += 40
            evidence.append(f"Low battery reserve detected ({min_battery}%)")
        else:
            evidence.append(f"Power subsystem nominal: {min_battery}% battery ({min_v:.1f}V)")

        if risk >= 75:
            severity = SeverityLevel.CRITICAL
            action = "SWITCH TO EMERGENCY SOLAR-BUFFERED LOW-POWER MODE"
        elif risk >= 40:
            severity = SeverityLevel.WARNING
            action = "SHED NON-CRITICAL TELEMETRY & PRESERVE SIREN RESERVE"
        else:
            severity = SeverityLevel.NORMAL
            action = "GRID / BATTERY RESERVES HEALTHY"

        return HazardAssessment(
            hazard_type=self.hazard_type,
            risk_score=min(100, risk),
            confidence=95,
            severity=severity,
            primary_metric="battery_pct",
            primary_value=float(min_battery),
            evidence=evidence,
            affected_zone="NODE POWER BUS",
            recommended_action=action
        )

# ---------------------------------------------------------------------------
# Hazard Module Registry
# ---------------------------------------------------------------------------

class HazardEngineRegistry:
    def __init__(self):
        self.modules: Dict[HazardType, BaseHazardModule] = {
            HazardType.FLASH_FLOOD: FloodHazardModule(),
            HazardType.FLOOD: FloodHazardModule(),
            HazardType.FIRE: FireHazardModule(),
            HazardType.GAS_LEAK: GasHazardModule(),
            HazardType.STRUCTURAL_ANOMALY: StructuralHazardModule(),
            HazardType.POWER_FAILURE: PowerHazardModule()
        }

    def evaluate_active_hazards(
        self,
        readings: List[NormalizedSensorReading],
        trust_map: Dict[str, float],
        profile: EnvironmentProfile
    ) -> List[HazardAssessment]:
        assessments = []
        for hazard_type in profile.active_hazards:
            module = self.modules.get(hazard_type)
            if module:
                assessment = module.evaluate(readings, trust_map, profile)
                if assessment:
                    assessments.append(assessment)
        return assessments

hazard_registry = HazardEngineRegistry()
