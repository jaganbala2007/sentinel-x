"""
Sentinel-X Hazard Zone Manager & Spatial Partitioning Engine
============================================================
Divides monitored facility into Zone A, Zone B, Zone C, and Zone D.
Tracks visual state (GREEN, AMBER, ORANGE, RED, GREY), sensor nodes, personnel,
and evacuation route accessibility.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.database import get_db_connection

class ZoneManager:
    def __init__(self):
        self.zones: Dict[str, Dict[str, Any]] = {
            "ZONE_A": {
                "zoneId": "ZONE_A",
                "name": "Zone A: Processing & Assembly Floor",
                "status": "NORMAL",
                "color": "GREEN",
                "hazardLevel": 0,
                "occupancy": 14,
                "sensorNodes": ["NODE-01"],
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "sensorHealth": "NORMAL",
                "incidentHistory": 0,
                "evacuationStatus": "SAFE"
            },
            "ZONE_B": {
                "zoneId": "ZONE_B",
                "name": "Zone B: Heavy Compressor & Gas Storage Bay",
                "status": "NORMAL",
                "color": "GREEN",
                "hazardLevel": 0,
                "occupancy": 6,
                "sensorNodes": ["NODE-02"],
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "sensorHealth": "NORMAL",
                "incidentHistory": 1,
                "evacuationStatus": "SAFE"
            },
            "ZONE_C": {
                "zoneId": "ZONE_C",
                "name": "Zone C: High-Voltage Electrical Switchgear Bay",
                "status": "NORMAL",
                "color": "GREEN",
                "hazardLevel": 0,
                "occupancy": 3,
                "sensorNodes": ["NODE-01", "NODE-02"],
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "sensorHealth": "NORMAL",
                "incidentHistory": 0,
                "evacuationStatus": "SAFE"
            },
            "ZONE_D": {
                "zoneId": "ZONE_D",
                "name": "Zone D: Outdoor Assembly Point & Emergency Exit Corridor",
                "status": "NORMAL",
                "color": "GREEN",
                "hazardLevel": 0,
                "occupancy": 2,
                "sensorNodes": ["GATEWAY-01"],
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "sensorHealth": "NORMAL",
                "incidentHistory": 0,
                "evacuationStatus": "PRIMARY_SAFE_ZONE"
            }
        }

    def update_zone_status(self, zone_id: str, status: str, hazard_level: int = 0, evacuation_status: str = None) -> Dict[str, Any]:
        zone_id = zone_id.upper()
        if zone_id not in self.zones:
            return {}

        color_map = {
            "NORMAL": "GREEN",
            "WATCH": "AMBER",
            "WARNING": "ORANGE",
            "CRITICAL": "RED",
            "OFFLINE": "GREY"
        }

        zone = self.zones[zone_id]
        zone["status"] = status
        zone["color"] = color_map.get(status, "GREEN")
        zone["hazardLevel"] = hazard_level
        zone["lastUpdate"] = datetime.now(timezone.utc).isoformat()
        if evacuation_status:
            zone["evacuationStatus"] = evacuation_status

        # Persist to database
        try:
            conn = get_db_connection()
            conn.execute(
                """INSERT OR REPLACE INTO zones (zone_id, name, status, hazard_level, occupancy, sensor_nodes, last_update)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (zone["zoneId"], zone["name"], zone["status"], zone["hazardLevel"], zone["occupancy"], ",".join(zone["sensorNodes"]), zone["lastUpdate"])
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        return zone

    def get_all_zones(self) -> Dict[str, Any]:
        return {
            "totalZones": len(self.zones),
            "zones": self.zones
        }

zone_manager = ZoneManager()
