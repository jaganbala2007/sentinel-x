/**
 * @file safety_controller.h
 * @brief Autonomous Local Edge Safety Controller for Sentinel-X Node
 * 
 * CORE PRINCIPLE:
 * RASPBERRY PI FAILURE != SAFETY FAILURE.
 * The node autonomously triggers physical siren relays and alarm beacons
 * when local hydrological emergency thresholds are exceeded, even if the
 * gateway is disconnected or destroyed.
 */

#pragma once

#include "sensor_manager.h"
#include <cstdint>

namespace Sentinel {

enum class SafetyState : uint8_t {
    NOMINAL = 0,
    WATCH = 1,
    WARNING = 2,
    EMERGENCY_CRITICAL = 3
};

class SafetyController {
public:
    SafetyController();
    bool init();

    // Evaluate local sensor reading and actuate hardware sirens if threshold breached
    SafetyState evaluate(const SensorReading& reading);

    SafetyState get_current_state() const { return current_state_; }
    bool is_siren_actuated() const { return siren_active_; }
    bool is_gateway_alive() const { return gateway_heartbeat_ok_; }

    // Heartbeat from Raspberry Pi 5 gateway
    void feed_gateway_heartbeat();

private:
    SafetyState current_state_;
    bool siren_active_;
    bool gateway_heartbeat_ok_;
    uint64_t last_gateway_heartbeat_ms_;

    // Configurable autonomous emergency thresholds
    static constexpr float STAGE_CRITICAL_THRESHOLD_M = 3.50f;
    static constexpr float RATE_CRITICAL_THRESHOLD_M_MIN = 0.06f;
    static constexpr uint64_t GATEWAY_TIMEOUT_MS = 15000; // 15 seconds without gateway = autonomous fallback

    void trigger_physical_siren(bool activate);
    void set_status_led(SafetyState state);
};

} // namespace Sentinel
