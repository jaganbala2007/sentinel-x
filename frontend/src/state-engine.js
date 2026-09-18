/**
 * Sentinel-X Central Reactive System State Engine
 * ===============================================
 * Single Source of Truth managing:
 *   - Hardware Abstraction Modes (LIVE, SIMULATION, OFFLINE)
 *   - Universal Risk Score & Multi-Signal Sensor Fusion
 *   - Worker Digital DNA (PPE Compliance, Proximity, Safety Profile)
 *   - Machine Safety DNA (PLC Lockout, Thermal/Vibration Baseline, Predictive RUL)
 *   - Sensor Mesh & Byzantine Reliability Verification
 *   - Incident Lifecycle Management
 *   - Disaster Communication State Machine
 *   - Immutable Audit Logging & Exporting
 * 
 * Version: 2.5.0
 * Author: Sentinel-X Principal Systems Engineering
 */

(function(window) {
    'use strict';

    class SentinelSystemState {
        constructor() {
            this.listeners = [];

            // Hardware Mode: 'SIMULATION' | 'LIVE' | 'OFFLINE'
            this.hardwareMode = 'SIMULATION';
            this.deploymentProfile = 'INDUSTRIAL'; // 'INDUSTRIAL' | 'NATURAL' | 'INFRASTRUCTURE' | 'ENVIRONMENTAL' | 'REMOTE'
            this.connectionStatus = 'ONLINE';
            this.commState = 'PRIMARY_INTERNET'; // 'PRIMARY_INTERNET' | 'HF_FAILOVER' | 'SATELLITE' | 'WAL_BUFFER'

            // Overall Safety State & Risk Scores (0-100)
            this.overallStatus = 'NORMAL'; // 'NORMAL' | 'WATCH' | 'WARNING' | 'CRITICAL' | 'EMERGENCY' | 'RECOVERY'
            this.riskScore = 14.8;
            this.environmentalRisk = 12.0;
            this.workerRisk = 8.4;
            this.machineRisk = 18.2;
            this.trustScore = 98.4;

            // Worker Digital DNA Registry
            this.workers = [
                {
                    id: "W-014",
                    name: "Rahul Sharma",
                    role: "Line Operator",
                    zone: "ZONE_A_CONVEYOR",
                    ppeStatus: "COMPLIANT", // 'COMPLIANT' | 'PARTIAL' | 'NON_COMPLIANT'
                    ppeDetails: { helmet: true, vest: true, boots: true, gloves: true },
                    safetyScore: 96.5,
                    exposureHours: 4.2,
                    trainingStatus: "CERTIFIED",
                    safetyState: "SAFE", // 'SAFE' | 'WARN' | 'DANGER'
                    heartRate: 78,
                    lastCheckin: "2 mins ago"
                },
                {
                    id: "W-022",
                    name: "Anil Kumar",
                    role: "Maintenance Engineer",
                    zone: "ZONE_B_COMPRESSOR",
                    ppeStatus: "COMPLIANT",
                    ppeDetails: { helmet: true, vest: true, boots: true, gloves: true },
                    safetyScore: 92.0,
                    exposureHours: 6.1,
                    trainingStatus: "CERTIFIED",
                    safetyState: "SAFE",
                    heartRate: 84,
                    lastCheckin: "5 mins ago"
                },
                {
                    id: "W-038",
                    name: "Priya Patel",
                    role: "Safety Officer",
                    zone: "ZONE_C_CONTROL",
                    ppeStatus: "COMPLIANT",
                    ppeDetails: { helmet: true, vest: true, boots: true, gloves: true },
                    safetyScore: 99.1,
                    exposureHours: 2.5,
                    trainingStatus: "MASTER_AUDITOR",
                    safetyState: "SAFE",
                    heartRate: 72,
                    lastCheckin: "1 min ago"
                }
            ];

            // Machine Safety DNA Registry
            this.machines = [
                {
                    id: "MTR-01",
                    name: "Primary Drive Motor MTR-01",
                    plcId: "PLC_CONVEYOR_01",
                    zone: "ZONE_A_CONVEYOR",
                    status: "RUNNING", // 'RUNNING' | 'IDLE' | 'WARNING' | 'CRITICAL' | 'ISOLATED'
                    motorTemp: 48.2,
                    vibrationHz: 1.2,
                    currentDrawA: 14.2,
                    beltSpeedMs: 1.5,
                    anomalyScore: 4.2,
                    predictedRULHours: 4280,
                    isLockedOut: false,
                    lastMaintenance: "2026-06-15"
                },
                {
                    id: "GBX-01",
                    name: "Helical Reduction Gearbox GBX-01",
                    plcId: "PLC_CONVEYOR_01",
                    zone: "ZONE_A_CONVEYOR",
                    status: "RUNNING",
                    motorTemp: 52.4,
                    vibrationHz: 2.1,
                    currentDrawA: 14.2,
                    beltSpeedMs: 1.5,
                    anomalyScore: 6.8,
                    predictedRULHours: 3890,
                    isLockedOut: false,
                    lastMaintenance: "2026-05-20"
                },
                {
                    id: "CMP-02",
                    name: "Auxiliary Air Compressor CMP-02",
                    plcId: "PLC_COMPRESSOR_B",
                    zone: "ZONE_B_COMPRESSOR",
                    status: "RUNNING",
                    motorTemp: 61.8,
                    vibrationHz: 3.4,
                    currentDrawA: 18.5,
                    beltSpeedMs: 0.0,
                    anomalyScore: 12.4,
                    predictedRULHours: 2150,
                    isLockedOut: false,
                    lastMaintenance: "2026-04-10"
                }
            ];

            // Sensor Telemetry Mesh & Reliability Ratings
            this.sensors = [
                { id: "PT100-01", name: "Thermal Resistance RTD", type: "TEMPERATURE", zone: "MTR-01", value: 48.2, unit: "°C", reliability: 98.4, state: "TRUSTED" },
                { id: "ADXL-01", name: "3-Axis Accelerometer", type: "VIBRATION", zone: "GBX-01", value: 1.2, unit: "mm/s", reliability: 99.1, state: "VERIFIED" },
                { id: "CT-101", name: "Induction Current Ring", type: "CURRENT", zone: "MTR-01", value: 14.2, unit: "A", reliability: 97.8, state: "NOMINAL" },
                { id: "MQ135-01", name: "Air Quality Gas Sensor", type: "GAS", zone: "ZONE_A", value: 210, unit: "PPM", reliability: 95.0, state: "NORMAL" },
                { id: "DHT22-01", name: "Ambient Temp & Humidity", type: "ENVIRONMENT", zone: "ZONE_A", value: 28.5, unit: "°C", reliability: 96.2, state: "NORMAL" },
                { id: "ENC-01", name: "Optical Tachometer", type: "SPEED", zone: "CONVEYOR", value: 1.5, unit: "m/s", reliability: 99.5, state: "MATCHED" }
            ];

            // Active Alerts List
            this.alerts = [
                {
                    id: "ALT-1001",
                    severity: "INFO", // 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
                    source: "SENSOR_TRUST_ENGINE",
                    zone: "ZONE_A_CONVEYOR",
                    message: "Sentinel-X Byzantine Sensor Mesh initialized. All 6 nodes synchronized.",
                    timestamp: new Date().toISOString(),
                    acknowledged: true,
                    acknowledgedBy: "admin@sentinel.x"
                }
            ];

            // Incident Lifecycle Tracker
            this.incidents = [];

            // Audit Event Log
            this.auditLog = [
                {
                    timestamp: new Date(Date.now() - 600000).toISOString(),
                    actor: "SYSTEM_BOOT",
                    action: "INITIALIZE_STATE_ENGINE",
                    target: "FACILITY_LINE_01",
                    previousState: "OFFLINE",
                    newState: "NORMAL",
                    reason: "Automated edge controller startup sequence completed."
                }
            ];

            // Current Active Scenario
            this.activeScenario = 'NORMAL';
            this.scenarioTimer = null;
        }

        // --- Subscription Pattern ---
        subscribe(callback) {
            if (typeof callback === 'function') {
                this.listeners.push(callback);
            }
        }

        notify() {
            this.listeners.forEach(cb => {
                try { cb(this); } catch (e) { console.error("[StateEngine] Listener error:", e); }
            });
        }

        // --- Hardware Mode Switcher ---
        async setHardwareMode(mode) {
            if (!['LIVE', 'SIMULATION', 'OFFLINE'].includes(mode)) return;
            const oldMode = this.hardwareMode;
            this.hardwareMode = mode;

            this.logAudit("OPERATOR", "SET_HARDWARE_MODE", "SYSTEM", oldMode, mode, `Operator changed telemetry mode to ${mode}`);

            // Call backend API if connected
            try {
                await fetch('/api/v1/telemetry-mode/mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: mode === 'LIVE' ? 'ONLINE' : mode === 'OFFLINE' ? 'OFFLINE' : 'ONLINE' })
                });
            } catch (e) {
                console.warn("[StateEngine] Mode API sync offline, using local state");
            }

            this.notify();
        }

        setDeploymentProfile(profile) {
            const valid = ['INDUSTRIAL', 'NATURAL', 'INFRASTRUCTURE', 'ENVIRONMENTAL', 'REMOTE'];
            if (!valid.includes(profile)) return;
            const old = this.deploymentProfile;
            this.deploymentProfile = profile;
            this.logAudit("OPERATOR", "SET_DEPLOYMENT_PROFILE", "SYSTEM", old, profile, `Site deployment profile changed to ${profile}`);
            this.notify();
        }

        // --- Audit Logging ---
        logAudit(actor, action, target, previousState, newState, reason) {
            const entry = {
                timestamp: new Date().toISOString(),
                actor: actor || "OPERATOR",
                action,
                target,
                previousState: String(previousState),
                newState: String(newState),
                reason
            };
            this.auditLog.unshift(entry);
            if (this.auditLog.length > 200) this.auditLog.pop();
        }

        // --- Incident Management Lifecycle ---
        createIncident(title, zone, trigger, severity, evidence) {
            const inc = {
                id: `INC-${Math.floor(100000 + Math.random() * 900000)}`,
                title,
                zone,
                trigger,
                severity: severity || "HIGH", // 'INFO' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
                state: "DETECTED", // 'DETECTED' | 'ACKNOWLEDGED' | 'INVESTIGATING' | 'CONTAINED' | 'RESOLVED'
                evidence: evidence || "Multi-signal sensor agreement",
                createdAt: new Date().toISOString(),
                resolvedAt: null,
                actionsTaken: []
            };
            this.incidents.unshift(inc);
            this.logAudit("SAFETY_ENGINE", "CREATE_INCIDENT", inc.id, "NOMINAL", "DETECTED", `${title} in ${zone}`);
            this.notify();
            return inc;
        }

        updateIncidentState(incidentId, newState, actor, note) {
            const inc = this.incidents.find(i => i.id === incidentId);
            if (!inc) return;
            const oldState = inc.state;
            inc.state = newState;
            inc.actionsTaken.push({ timestamp: new Date().toISOString(), actor, action: newState, note });
            if (newState === 'RESOLVED') inc.resolvedAt = new Date().toISOString();

            this.logAudit(actor || "OPERATOR", "UPDATE_INCIDENT_STATE", inc.id, oldState, newState, note || `Incident status set to ${newState}`);
            this.notify();
        }

        // --- Alert Management ---
        addAlert(severity, source, zone, message) {
            const alert = {
                id: `ALT-${Math.floor(1000 + Math.random() * 9000)}`,
                severity,
                source,
                zone,
                message,
                timestamp: new Date().toISOString(),
                acknowledged: false,
                acknowledgedBy: null
            };
            this.alerts.unshift(alert);
            this.notify();
            return alert;
        }

        acknowledgeAlert(alertId, user = "admin@sentinel.x") {
            const alt = this.alerts.find(a => a.id === alertId);
            if (alt) {
                alt.acknowledged = true;
                alt.acknowledgedBy = user;
                this.logAudit(user, "ACKNOWLEDGE_ALERT", alt.id, "UNACKNOWLEDGED", "ACKNOWLEDGED", alt.message);
                this.notify();
            }
        }

        // --- Operator Commands ---
        isolateMachine(machineId, actor = "OPERATOR") {
            const m = this.machines.find(x => x.id === machineId);
            if (!m) return;
            const oldStatus = m.status;
            m.status = "ISOLATED";
            m.isLockedOut = true;
            m.beltSpeedMs = 0.0;
            m.currentDrawA = 0.0;

            this.logAudit(actor, "PLC_LOCKOUT_ISOLATE", m.id, oldStatus, "ISOLATED", `Modbus 415V Relay Lockout triggered for ${m.name}`);
            this.addAlert("HIGH", "OPERATOR_COMMAND", m.zone, `Machine ${m.name} emergency isolated by ${actor}`);
            
            // Sync backend API
            fetch('/api/v1/machine/lockout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ machine_id: m.plcId || "PLC_CONVEYOR_01", reason: "Operator Isolation", operator_id: actor })
            }).catch(() => {});

            this.recalculateRisk();
            this.notify();
        }

        evacuateZone(zoneName, actor = "OPERATOR") {
            this.workers.filter(w => w.zone === zoneName).forEach(w => {
                w.safetyState = "DANGER";
            });
            this.overallStatus = "EMERGENCY";
            this.logAudit(actor, "EVACUATE_ZONE", zoneName, "SAFE", "EVACUATING", `Zone ${zoneName} Emergency Evacuation Command Issued`);
            this.createIncident("Zone Emergency Evacuation", zoneName, "OPERATOR_OVERRIDE", "CRITICAL", `Evacuation ordered by ${actor}`);
            this.notify();
        }

        warnWorker(workerId, message, actor = "OPERATOR") {
            const w = this.workers.find(x => x.id === workerId);
            if (!w) return;
            w.safetyState = "WARN";
            this.logAudit(actor, "WARN_WORKER", w.id, "SAFE", "WARN", `Smart Tag warning issued: ${message}`);
            this.notify();
        }

        tripEmergencyStop(reason = "Operator E-Stop Button Pressed", actor = "OPERATOR") {
            this.machines.forEach(m => {
                m.status = "ISOLATED";
                m.isLockedOut = true;
                m.beltSpeedMs = 0.0;
                m.currentDrawA = 0.0;
            });
            this.overallStatus = "CRITICAL";
            this.riskScore = 94.0;
            this.logAudit(actor, "HARDWARE_ESTOP_TRIP", "PLANT_LINE_01", "NOMINAL", "E_STOP_TRIPPED", reason);
            this.createIncident("415V Hardware Emergency Stop", "PLANT_LINE_01", "PHYSICAL_ESTOP", "CRITICAL", reason);
            this.notify();
        }

        resetSystem(actor = "OPERATOR") {
            this.machines.forEach(m => {
                m.status = "RUNNING";
                m.isLockedOut = false;
                m.motorTemp = 48.2;
                m.vibrationHz = 1.2;
                m.currentDrawA = 14.2;
                m.beltSpeedMs = 1.5;
                m.anomalyScore = 4.2;
            });
            this.workers.forEach(w => {
                w.safetyState = "SAFE";
                w.ppeStatus = "COMPLIANT";
            });
            this.sensors.forEach(s => {
                s.state = "TRUSTED";
                s.reliability = 98.4;
            });
            this.overallStatus = "NORMAL";
            this.riskScore = 14.8;
            this.commState = "PRIMARY_INTERNET";
            this.logAudit(actor, "SYSTEM_RESET_NOMINAL", "PLANT_LINE_01", "EMERGENCY/FAULT", "NORMAL", "System restored to normal operating baseline.");
            this.notify();
        }

        // --- Disaster Scenario Engine ---
        executeScenario(scenarioKey) {
            this.activeScenario = scenarioKey;
            if (scenarioKey === 'NORMAL') {
                this.resetSystem("SIMULATION_ENGINE");
            } else if (scenarioKey === 'GAS_LEAK') {
                this.overallStatus = "WARNING";
                this.riskScore = 64.5;
                this.environmentalRisk = 78.0;
                const mq = this.sensors.find(s => s.id === 'MQ135-01');
                if (mq) { mq.value = 840; mq.state = "HAZARD_ELEVATED"; }
                this.addAlert("HIGH", "MQ135_GAS_SENSOR", "ZONE_A_CONVEYOR", "Hazardous gas concentration elevated (840 PPM). Zone ventilation required.");
                this.createIncident("Environmental Gas Leak Anomaly", "ZONE_A_CONVEYOR", "MQ135_THRESHOLD", "HIGH", "MQ-135 reading 840 PPM correlated with thermal RTD.");
                this.logAudit("SIMULATION", "TRIGGER_SCENARIO", "GAS_LEAK", "NORMAL", "WARNING", "Injected Gas Leak Scenario");
            } else if (scenarioKey === 'OVERHEAT') {
                this.overallStatus = "CRITICAL";
                this.riskScore = 88.0;
                this.machineRisk = 92.0;
                const mtr = this.machines.find(m => m.id === 'MTR-01');
                if (mtr) { mtr.status = "CRITICAL"; mtr.motorTemp = 94.2; mtr.currentDrawA = 22.8; }
                const pt = this.sensors.find(s => s.id === 'PT100-01');
                if (pt) { pt.value = 94.2; pt.state = "OVERHEAT"; }
                this.tripEmergencyStop("Drive Motor MTR-01 thermal limit exceeded (94.2°C).", "AUTONOMOUS_INTERLOCK");
            } else if (scenarioKey === 'VIBRATION') {
                this.overallStatus = "WARNING";
                this.riskScore = 58.2;
                this.machineRisk = 68.0;
                const gbx = this.machines.find(m => m.id === 'GBX-01');
                if (gbx) { gbx.status = "WARNING"; gbx.vibrationHz = 8.4; gbx.anomalyScore = 74.2; }
                const adxl = this.sensors.find(s => s.id === 'ADXL-01');
                if (adxl) { adxl.value = 8.4; adxl.state = "VIBRATION_WARNING"; }
                this.addAlert("MEDIUM", "ADXL345_ACCEL", "GBX-01", "Gearbox GBX-01 mechanical vibration exceeded ISO 10816 Class II threshold (8.4 mm/s).");
                this.logAudit("SIMULATION", "TRIGGER_SCENARIO", "VIBRATION_FAULT", "NORMAL", "WARNING", "Injected Mechanical Vibration Failure");
            } else if (scenarioKey === 'PPE_VIOLATION') {
                const w = this.workers.find(x => x.id === 'W-014');
                if (w) {
                    w.ppeStatus = "NON_COMPLIANT";
                    w.ppeDetails.helmet = false;
                    w.safetyState = "WARN";
                }
                this.addAlert("MEDIUM", "PREDSHIELD_VISION_AI", "ZONE_A_CONVEYOR", "PPE Non-Compliance: Worker W-014 (Rahul Sharma) missing hardhat in active conveyor area.");
                this.logAudit("PREDSHIELD_AI", "PPE_VIOLATION_DETECTED", "W-014", "COMPLIANT", "NON_COMPLIANT", "Computer Vision confirmed missing safety hardhat");
            } else if (scenarioKey === 'SENSOR_SPOOF') {
                const pt = this.sensors.find(s => s.id === 'PT100-01');
                if (pt) { pt.value = 92.4; pt.reliability = 12.0; pt.state = "QUARANTINED_SPOOF"; }
                this.trustScore = 74.2;
                this.addAlert("HIGH", "BYZANTINE_TRUST_ENGINE", "PT100-01", "Sensor Discordance: PT100 reports 92.4°C while vibration is 1.2 mm/s and current is 14.2A. Quarantined.");
                this.logAudit("BYZANTINE_ENGINE", "QUARANTINE_SENSOR", "PT100-01", "TRUSTED", "QUARANTINED", "Byzantine evidence isolation prevented false plant trip.");
            } else if (scenarioKey === 'NETWORK_CUT') {
                this.commState = 'HF_FAILOVER';
                this.addAlert("WARNING", "COMM_MANAGER", "SYSTEM", "WAN Primary Internet connection severed. Failover to HF Packet Radio (7.105 MHz AX.25).");
                this.logAudit("RESILIENCE_ENGINE", "FAILOVER_COMM", "HF_RADIO", "PRIMARY_INTERNET", "HF_FAILOVER", "Automatic disaster communication failover");
            }

            this.recalculateRisk();
            this.notify();
        }

        recalculateRisk() {
            let maxMtrRisk = Math.max(...this.machines.map(m => m.anomalyScore || 0));
            let unackAlerts = this.alerts.filter(a => !a.acknowledged).length;
            this.riskScore = Math.min(100, Math.max(10, (maxMtrRisk * 0.4) + (unackAlerts * 8) + (this.overallStatus === 'CRITICAL' ? 50 : 0)));
        }

        // --- Disaster Management API Integration Methods ---
        async triggerDisasterScenario(scenarioId) {
            try {
                const res = await fetch(`/api/v1/disasters/scenarios/${scenarioId}/trigger`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ step_index: 2 })
                });
                const data = await res.json();
                this.addAlert("HIGH", "DISASTER_SCENARIO_ENGINE", data.incident ? data.incident.zone : "ZONE_B", `Disaster Scenario Triggered: ${scenarioId}`);
                this.logAudit(this.currentRole || "COMMANDER", "TRIGGER_DISASTER_SCENARIO", scenarioId, "NORMAL", "CRITICAL", `Triggered ${scenarioId}`);
                this.recalculateRisk();
                this.notify();
                return data;
            } catch (err) {
                console.warn("Backend scenario trigger fallback:", err);
            }
        }

        async ackIncident(incidentId) {
            try {
                const res = await fetch(`/api/v1/incidents/${incidentId}/acknowledge`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ operator: this.currentRole || "COMMANDER" })
                });
                const data = await res.json();
                this.logAudit(this.currentRole || "COMMANDER", "ACKNOWLEDGE_INCIDENT", incidentId, "DETECTED", "ACKNOWLEDGED", "Commander acknowledged disaster incident");
                this.notify();
                return data;
            } catch (err) {
                console.warn("Ack incident fallback:", err);
            }
        }

        async assignTeam(incidentId, teamId) {
            try {
                const res = await fetch(`/api/v1/incidents/${incidentId}/assign`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ team_id: teamId, operator: this.currentRole || "COMMANDER" })
                });
                const data = await res.json();
                this.logAudit(this.currentRole || "COMMANDER", "ASSIGN_RESPONSE_RESOURCE", teamId, "AVAILABLE", "DEPLOYED", `Assigned ${teamId} to ${incidentId}`);
                this.notify();
                return data;
            } catch (err) {
                console.warn("Assign team fallback:", err);
            }
        }

        async triggerEvacuation(zoneId) {
            try {
                const res = await fetch(`/api/v1/incidents/INC-8901/evacuate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ zone_id: zoneId })
                });
                const data = await res.json();
                this.logAudit(this.currentRole || "COMMANDER", "TRIGGER_ZONE_EVACUATION", zoneId, "SAFE", "EVACUATE", `Evacuation triggered for ${zoneId}`);
                this.notify();
                return data;
            } catch (err) {
                console.warn("Evacuation fallback:", err);
            }
        }

        async resetAll(actor = "COMMANDER") {
            try {
                await fetch('/api/v1/sih-demo/reset', { method: 'POST' });
            } catch (e) {
                console.warn("[StateEngine] Backend reset fallback:", e);
            }
            this.resetSystem(actor);
            this.incidents = [];
            this.activeScenario = 'NORMAL';
            this.overallStatus = 'NORMAL';
            this.riskScore = 0;
            this.logAudit(actor, "RESET_ALL_DISASTER_STATE", "SYSTEM", "ANY", "NORMAL", "Complete system reset triggered.");
            this.notify();
        }

        async resolveIncident(incidentId) {
            try {
                const res = await fetch(`/api/v1/incidents/${incidentId}/resolve`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ operator: this.currentRole || "COMMANDER" })
                });
                const data = await res.json();
                this.logAudit(this.currentRole || "COMMANDER", "RESOLVE_INCIDENT", incidentId, "CRITICAL", "RESOLVED", `Incident ${incidentId} resolved and report generated`);
                this.notify();
                return data;
            } catch (err) {
                console.warn("Resolve incident fallback:", err);
            }
        }

        // --- Export Reports ---
        exportData(format = 'json') {
            const data = {
                timestamp: new Date().toISOString(),
                system: "SENTINEL-X",
                systemTitle: "Edge-AI Disaster Resilience, Situational Awareness & Response System",
                hardwareMode: this.hardwareMode,
                overallStatus: this.overallStatus,
                riskScore: this.riskScore,
                trustScore: this.trustScore,
                commState: this.commState,
                workers: this.workers,
                machines: this.machines,
                sensors: this.sensors,
                alerts: this.alerts,
                incidents: this.incidents,
                auditLog: this.auditLog
            };

            if (format === 'json') {
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `sentinel_x_disaster_report_${Date.now()}.json`;
                a.click();
            } else if (format === 'csv') {
                let csv = "Timestamp,Section,Item,Status,Value,Details\n";
                this.sensors.forEach(s => {
                    csv += `"${new Date().toISOString()}","SENSOR","${s.name}","${s.state}","${s.value} ${s.unit}","Reliability ${s.reliability}%"\n`;
                });
                this.machines.forEach(m => {
                    csv += `"${new Date().toISOString()}","MACHINE","${m.name}","${m.status}","${m.motorTemp}°C","Vibration ${m.vibrationHz}mm/s, Current ${m.currentDrawA}A"\n`;
                });
                this.workers.forEach(w => {
                    csv += `"${new Date().toISOString()}","WORKER","${w.name} (${w.id})","${w.safetyState}","PPE ${w.ppeStatus}","Zone ${w.zone}"\n`;
                });
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `sentinel_x_disaster_telemetry_${Date.now()}.csv`;
                a.click();
            }
        }
    }

    // Export Singleton Instance
    window.SentinelState = new SentinelSystemState();

})(window);

