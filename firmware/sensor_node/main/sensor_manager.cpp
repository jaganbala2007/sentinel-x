/**
 * @file sensor_manager.cpp
 * @brief Implementation of sensor acquisition & plausibility checking
 */

#include "sensor_manager.h"
#include <cstring>
#include <cmath>

#if defined(ESP_PLATFORM)
#include "esp_timer.h"
#include "esp_log.h"
static const char* TAG = "SensorManager";
#else
#include <chrono>
#endif

namespace Sentinel {

SensorManager::SensorManager() 
    : previous_water_level_m_(2.40f),
      previous_sample_ms_(0),
      sequence_counter_(0) {
    std::memset(&latest_reading_, 0, sizeof(SensorReading));
    std::strncpy(latest_reading_.node_id, "NODE-01", sizeof(latest_reading_.node_id) - 1);
}

bool SensorManager::init() {
    // Hardware peripheral initialization (ADC, I2C bus for BMP388/AHT20, UART for Radar stage sensor)
    previous_sample_ms_ = 0;
    sequence_counter_ = 0;
    latest_reading_.sensor_health_flags = 0x000F; // All 4 sensors nominal
    return true;
}

float SensorManager::read_water_level_sensor() {
    // In hardware mode: reads Modbus RS485 / 4-20mA Radar stage meter
    // In prototype/simulation mode: baseline with gentle diurnal variation
    return 2.41f + 0.02f * std::sin(sequence_counter_ * 0.1f);
}

float SensorManager::read_barometric_pressure() {
    // BMP388 / BME280 I2C reading
    return 1013.25f - 0.5f * std::sin(sequence_counter_ * 0.05f);
}

float SensorManager::read_soil_saturation() {
    // TDR probe analog output
    return 48.5f + 2.0f * std::cos(sequence_counter_ * 0.08f);
}

float SensorManager::read_battery_voltage() {
    // ADC divider on LiFePO4 battery cell
    return 3.32f;
}

bool SensorManager::is_physically_plausible(float stage, float rate_of_rise) const {
    // Hydrodynamic rate limits: In Sector B river basin, natural water level cannot rise faster
    // than 0.25 m/min without an instantaneous flash breach.
    if (stage < 0.0f || stage > 15.0f) {
        return false; // Impossible elevation relative to datum
    }
    if (std::abs(rate_of_rise) > 0.50f) {
        return false; // Physical plausibility violation (sensor impulse / electrical noise)
    }
    return true;
}

bool SensorManager::sample_all() {
    uint64_t current_ms = 0;
#if defined(ESP_PLATFORM)
    current_ms = esp_timer_get_time() / 1000;
#else
    current_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
#endif

    float current_stage = read_water_level_sensor();
    
    // Calculate rate of rise (m / min)
    float dt_min = (previous_sample_ms_ > 0) ? ((current_ms - previous_sample_ms_) / 60000.0f) : 1.0f / 60.0f;
    if (dt_min <= 0.0f) dt_min = 1.0f / 60.0f;
    
    float rate_of_rise = (current_stage - previous_water_level_m_) / dt_min;

    latest_reading_.timestamp_ms = current_ms;
    latest_reading_.water_level_m = current_stage;
    latest_reading_.rate_of_rise_m_min = rate_of_rise;
    latest_reading_.baro_pressure_hpa = read_barometric_pressure();
    latest_reading_.temperature_c = 26.4f;
    latest_reading_.humidity_pct = 78.2f;
    latest_reading_.soil_saturation_pct = read_soil_saturation();
    latest_reading_.battery_voltage_v = read_battery_voltage();
    latest_reading_.battery_pct = 94;
    latest_reading_.sequence_num = ++sequence_counter_;

    // Set confidence based on physical bounds
    if (is_physically_plausible(current_stage, rate_of_rise)) {
        latest_reading_.confidence = 0.98f;
    } else {
        latest_reading_.confidence = 0.25f;
        latest_reading_.sensor_health_flags &= ~0x0001; // Flag stage sensor suspect
    }

    previous_water_level_m_ = current_stage;
    previous_sample_ms_ = current_ms;

    return true;
}

} // namespace Sentinel
