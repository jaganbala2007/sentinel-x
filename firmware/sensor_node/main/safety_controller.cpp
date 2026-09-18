/**
 * @file safety_controller.cpp
 * @brief Implementation of autonomous local safety actuation
 */

#include "safety_controller.h"
#include <cstdio>

#if defined(ESP_PLATFORM)
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"
static const char* TAG = "SafetyController";
#define PIN_SIREN_RELAY GPIO_NUM_18
#define PIN_LED_ALERT   GPIO_NUM_19
#else
#include <chrono>
#endif

namespace Sentinel {

SafetyController::SafetyController()
    : current_state_(SafetyState::NOMINAL),
      siren_active_(false),
      gateway_heartbeat_ok_(true),
      last_gateway_heartbeat_ms_(0) {}

bool SafetyController::init() {
#if defined(ESP_PLATFORM)
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_SIREN_RELAY) | (1ULL << PIN_LED_ALERT);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);
    
    gpio_set_level(PIN_SIREN_RELAY, 0);
    gpio_set_level(PIN_LED_ALERT, 0);
#endif
    return true;
}

void SafetyController::feed_gateway_heartbeat() {
    uint64_t current_ms = 0;
#if defined(ESP_PLATFORM)
    current_ms = esp_timer_get_time() / 1000;
#else
    current_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
#endif
    last_gateway_heartbeat_ms_ = current_ms;
    gateway_heartbeat_ok_ = true;
}

void SafetyController::trigger_physical_siren(bool activate) {
    siren_active_ = activate;
#if defined(ESP_PLATFORM)
    gpio_set_level(PIN_SIREN_RELAY, activate ? 1 : 0);
    ESP_LOGW(TAG, "AUTONOMOUS ACTUATOR: Siren relay set to %d", activate ? 1 : 0);
#else
    printf("[AUTONOMOUS ACTUATOR] Local hardware siren relay: %s\n", activate ? "ACTIVE (105 dB)" : "IDLE");
#endif
}

void SafetyController::set_status_led(SafetyState state) {
#if defined(ESP_PLATFORM)
    gpio_set_level(PIN_LED_ALERT, (state == SafetyState::EMERGENCY_CRITICAL) ? 1 : 0);
#endif
}

SafetyState SafetyController::evaluate(const SensorReading& reading) {
    uint64_t current_ms = 0;
#if defined(ESP_PLATFORM)
    current_ms = esp_timer_get_time() / 1000;
#else
    current_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
#endif

    // 1. Check if Raspberry Pi 5 gateway has gone silent
    if (last_gateway_heartbeat_ms_ > 0 && (current_ms - last_gateway_heartbeat_ms_) > GATEWAY_TIMEOUT_MS) {
        gateway_heartbeat_ok_ = false;
        // Node enters Autonomous Edge Blackout Mode
    }

    // 2. Local Safety Decision Matrix
    // Note: If confidence is low (< 0.5), we do NOT fire false emergency alarms from a single erratic sensor.
    if (reading.confidence >= 0.5f) {
        if (reading.water_level_m >= STAGE_CRITICAL_THRESHOLD_M || reading.rate_of_rise_m_min >= RATE_CRITICAL_THRESHOLD_M_MIN) {
            current_state_ = SafetyState::EMERGENCY_CRITICAL;
            trigger_physical_siren(true);
        } else if (reading.water_level_m >= (STAGE_CRITICAL_THRESHOLD_M * 0.85f)) {
            current_state_ = SafetyState::WARNING;
            trigger_physical_siren(false);
        } else {
            current_state_ = SafetyState::NOMINAL;
            trigger_physical_siren(false);
        }
    }

    set_status_led(current_state_);
    return current_state_;
}

} // namespace Sentinel
