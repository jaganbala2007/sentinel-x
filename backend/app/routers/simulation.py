"""
Simulation & 5 SIH Hero Demonstrations Router
"""

from fastapi import APIRouter
from app.schemas.disaster import SimulationInjectSchema
from app.services.sensor_trust_engine import sensor_trust_engine
from app.services.disaster_fusion_engine import disaster_fusion_engine
from app.services.communication_manager import communication_manager
from app.services.store_and_forward import store_and_forward_service

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation & SIH Scenarios"])

@router.post("/inject")
def inject_simulation_scenario(payload: SimulationInjectSchema):
    scenario = payload.scenario

    if scenario == "disaster_detection":
        disaster_fusion_engine.current_risk_score = 84
        disaster_fusion_engine.current_severity = "CRITICAL"
        disaster_fusion_engine.current_confidence = 94
        return {"scenario": scenario, "result": "HERO 1 ACTIVE: Real disaster surge triggered at Sector B"}

    elif scenario == "sensor_spoofing":
        sensor_trust_engine.evaluate_node("NODE-03", current_stage=8.90, rate_of_rise=2.45, neighbor_readings=[2.41, 2.42])
        return {"scenario": scenario, "result": "HERO 2 ACTIVE: Node-03 injected with 8.90m reading; quarantined"}

    elif scenario == "internet_failure":
        communication_manager.set_mode("DEGRADED")
        return {"scenario": scenario, "result": "HERO 3 ACTIVE: Internet cut; sub-50ms failover to 7.105 MHz HF Packet Radio"}

    elif scenario == "complete_network_loss":
        communication_manager.set_mode("ISOLATED")
        # Queue 17 events in local SQLite
        for i in range(1, 18):
            store_and_forward_service.queue_event(
                node_id="NODE-02",
                event_type="TELEMETRY_SNAP",
                severity="HIGH",
                risk_score=84,
                confidence=94,
                payload={"stage_m": 3.85, "packet_idx": i}
            )
        return {"scenario": scenario, "result": "HERO 4 ACTIVE: Total blackout; autonomous edge safety continues; 17 events queued in local SQLite"}

    elif scenario == "restoration":
        communication_manager.set_mode("NORMAL")
        sync_res = store_and_forward_service.sync_all_pending()
        return {"scenario": scenario, "result": "HERO 5 ACTIVE: Backhaul restored; synchronized queued events", "sync_details": sync_res}

    elif scenario == "reset_normal":
        communication_manager.set_mode("NORMAL")
        disaster_fusion_engine.current_risk_score = 18
        disaster_fusion_engine.current_severity = "NORMAL"
        disaster_fusion_engine.current_confidence = 96
        for i in range(1, 21):
            sensor_trust_engine.evaluate_node(f"NODE-{i:02d}", current_stage=2.41, rate_of_rise=0.01, neighbor_readings=[2.41])
        store_and_forward_service.clear_all()
        return {"scenario": scenario, "result": "RESET: System restored to steady-state operational monitoring"}

    return {"error": f"Unknown scenario: {scenario}"}
