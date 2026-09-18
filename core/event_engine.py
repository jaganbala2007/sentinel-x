"""
Sentinel-X Core: Event Correlation & Logging Engine
===================================================
Produces structured, sequence-numbered events for safety audits, store-and-forward,
and cross-environment history.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SafetyEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    timestamp: float = Field(default_factory=time.time)
    source: str = "RPI5-EDGE-01"
    environment: str = "INDUSTRIAL"
    hazard: str = "EQUIPMENT"
    risk_score: float = 0.0
    priority: str = "INFO" # INFO, WATCH, WARNING, CRITICAL
    payload: Dict[str, Any] = Field(default_factory=dict)
    sequence_num: int = 0
    status: str = "PENDING" # PENDING, SENT, FAILED, SYNCHRONIZED

class EventEngine:
    def __init__(self):
        self._sequence_counter = 0
        self._event_log: List[SafetyEvent] = []

    def create_event(self, environment: str, hazard: str, risk_score: float, 
                     priority: str, payload: Dict[str, Any], source: str = "RPI5-EDGE-01") -> SafetyEvent:
        self._sequence_counter += 1
        event = SafetyEvent(
            source=source,
            environment=environment,
            hazard=hazard,
            risk_score=round(risk_score, 1),
            priority=priority,
            payload=payload,
            sequence_num=self._sequence_counter,
            status="PENDING"
        )
        self._event_log.append(event)
        # Keep last 500 events in memory
        if len(self._event_log) > 500:
            self._event_log.pop(0)
        return event

    def get_recent_events(self, limit: int = 50) -> List[SafetyEvent]:
        return self._event_log[-limit:]

event_engine = EventEngine()
SafetyEventEngine = EventEngine
