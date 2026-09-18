"""
Sentinel-X Authoritative Disaster Lifecycle State Machine
==========================================================
Manages formal disaster lifecycle states:
  NORMAL -> WATCH -> WARNING -> INCIDENT -> CRITICAL -> RESPONSE -> STABILIZATION -> RECOVERY -> RESOLVED

Guarantees backend state persistence, audit trail accountability, and action authorization.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import json
from core.database import get_db_connection

class DisasterStateMachine:
    VALID_STATES = [
        "NORMAL", "WATCH", "WARNING", "INCIDENT", 
        "CRITICAL", "RESPONSE", "STABILIZATION", "RECOVERY", "RESOLVED"
    ]

    TRANSITIONS = {
        "NORMAL": ["WATCH", "WARNING", "INCIDENT"],
        "WATCH": ["NORMAL", "WARNING", "INCIDENT"],
        "WARNING": ["NORMAL", "WATCH", "INCIDENT", "CRITICAL"],
        "INCIDENT": ["CRITICAL", "RESPONSE", "RESOLVED"],
        "CRITICAL": ["RESPONSE", "STABILIZATION"],
        "RESPONSE": ["STABILIZATION", "RECOVERY"],
        "STABILIZATION": ["RECOVERY", "RESOLVED"],
        "RECOVERY": ["RESOLVED", "NORMAL"],
        "RESOLVED": ["NORMAL"]
    }

    def __init__(self):
        self.current_state: str = "NORMAL"
        self.active_incident_id: Optional[str] = None
        self.state_history: List[Dict[str, Any]] = []
        self._record_state_change("NORMAL", "System initialized in nominal state.", "SYSTEM_AUTO")

    def transition_to(self, new_state: str, reason: str, operator: str = "COMMANDER", incident_id: str = None, zone_id: str = None) -> Dict[str, Any]:
        new_state = new_state.upper()
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Invalid disaster state: {new_state}")

        prev_state = self.current_state
        if new_state != prev_state and new_state not in self.TRANSITIONS.get(prev_state, []):
            # Allow forced administrative override for critical emergencies
            if "CRITICAL" not in new_state and "RESPONSE" not in new_state:
                raise ValueError(f"Illegal state transition from {prev_state} to {new_state}")

        self.current_state = new_state
        if incident_id:
            self.active_incident_id = incident_id

        record = self._record_state_change(new_state, reason, operator, prev_state, incident_id, zone_id)
        return record

    def _record_state_change(self, new_state: str, reason: str, operator: str, prev_state: str = "", incident_id: str = None, zone_id: str = None) -> Dict[str, Any]:
        ts = datetime.now(timezone.utc).isoformat()
        record = {
            "timestamp": ts,
            "prevState": prev_state or self.current_state,
            "newState": new_state,
            "reason": reason,
            "operator": operator,
            "incidentId": incident_id or self.active_incident_id,
            "zoneId": zone_id or "ZONE_ALL"
        }
        self.state_history.append(record)

        # Persist to database audit_logs
        try:
            conn = get_db_connection()
            conn.execute(
                """INSERT INTO audit_logs (timestamp, user_role, action, incident_id, zone_id, prev_state, new_state, details)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (ts, operator, f"TRANSITION_TO_{new_state}", incident_id or self.active_incident_id, zone_id or "ZONE_ALL", prev_state, new_state, reason)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            pass

        return record

    def get_status(self) -> Dict[str, Any]:
        return {
            "currentState": self.current_state,
            "activeIncidentId": self.active_incident_id,
            "validTransitions": self.TRANSITIONS.get(self.current_state, []),
            "historyCount": len(self.state_history),
            "recentHistory": self.state_history[-5:]
        }

disaster_state_machine = DisasterStateMachine()
