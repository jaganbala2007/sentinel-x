"""
Sentinel-X Evacuation & Resource Coordination Engine
=====================================================
Manages spatial evacuation routes, safe exit paths, blocked hazard corridors,
and emergency response resource tracking.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.database import get_db_connection

class EvacuationManager:
    def __init__(self):
        self.evacuation_mode_active: bool = False
        self.affected_zones: List[str] = []
        self.safe_zones: List[str] = ["ZONE_D"]
        self.blocked_routes: List[str] = []
        
        self.routes = [
            {"id": "ROUTE-A-D", "from": "ZONE_A", "to": "ZONE_D", "name": "Main Corridor North Exit", "status": "CLEAR", "distance": "45m"},
            {"id": "ROUTE-B-D", "from": "ZONE_B", "to": "ZONE_D", "name": "East Compressor Bay Exit", "status": "CLEAR", "distance": "60m"},
            {"id": "ROUTE-C-D", "from": "ZONE_C", "to": "ZONE_D", "name": "Switchgear Emergency Tunnel", "status": "CLEAR", "distance": "30m"}
        ]

        self.resources = [
            {"id": "RES-01", "name": "Alpha Hazmat Response Team", "type": "RESPONSE_TEAM", "status": "AVAILABLE", "assignedIncident": None, "location": "Zone D Staging"},
            {"id": "RES-02", "name": "Bravo Medical First-Aid Kit", "type": "FIRST_AID", "status": "AVAILABLE", "assignedIncident": None, "location": "Zone A Depot"},
            {"id": "RES-03", "name": "Gamma Heavy Fire Extinguisher", "type": "EQUIPMENT", "status": "AVAILABLE", "assignedIncident": None, "location": "Zone B Bay"},
            {"id": "RES-04", "name": "Delta Edge Mesh Comms Node", "type": "COMMS", "status": "AVAILABLE", "assignedIncident": None, "location": "RPI-4 Command Unit"}
        ]

    def trigger_evacuation(self, zone_id: str, hazard_type: str = "HAZARD") -> Dict[str, Any]:
        self.evacuation_mode_active = True
        zone_id = zone_id.upper()
        if zone_id not in self.affected_zones:
            self.affected_zones.append(zone_id)

        # Mark corresponding exit route as RESTRICTED/BLOCKED if in direct hazard zone
        for route in self.routes:
            if route["from"] == zone_id:
                route["status"] = "RESTRICTED"

        return self.get_evacuation_state()

    def reset_evacuation(self) -> Dict[str, Any]:
        self.evacuation_mode_active = False
        self.affected_zones = []
        self.blocked_routes = []
        for route in self.routes:
            route["status"] = "CLEAR"
        return self.get_evacuation_state()

    def assign_resource(self, resource_id: str, incident_id: str) -> Dict[str, Any]:
        for res in self.resources:
            if res["id"] == resource_id:
                res["status"] = "DEPLOYED"
                res["assignedIncident"] = incident_id
                return res
        return {}

    def release_resource(self, resource_id: str) -> Dict[str, Any]:
        for res in self.resources:
            if res["id"] == resource_id:
                res["status"] = "AVAILABLE"
                res["assignedIncident"] = None
                return res
        return {}

    def get_evacuation_state(self) -> Dict[str, Any]:
        return {
            "evacuationModeActive": self.evacuation_mode_active,
            "affectedZones": self.affected_zones,
            "safeZones": self.safe_zones,
            "blockedRoutes": self.blocked_routes,
            "routes": self.routes,
            "resources": self.resources
        }

evacuation_manager = EvacuationManager()
