/**
 * @file sensor_manager.h
 * @brief Normalized Sensor Abstraction for Sentinel-X ESP32-S3 Node
 */

#pragma once

#include <cstdint>
#include <cstddef>

namespace Sentinel {

struct SensorReading {
    char node_id[16];
    uint64_t timestamp_ms;
    float water_level_m;
    float rate_of_rise_m_min;
    float baro_pressure_hpa;
    float temperature_c;
    float humidity_pct;
    float soil_saturation_pct;
    float battery_voltage_v;
    uint8_t battery_pct;
    uint16_t sensor_health_flags; // Bit 0: Water gauge, Bit 1: Baro, Bit 2: TDR Soil, Bit 3: ADC
    float confidence;             // 0.0 - 1.0 based on physical plausibility
    uint32_t sequence_num;
};

class SensorManager {
public:
    SensorManager();
    bool init();
    bool sample_all();
    const SensorReading& get_latest_reading() const { return latest_reading_; }
    
    // Physics bounds verification
    bool is_physically_plausible(float stage, float rate_of_rise) const;

private:
    SensorReading latest_reading_;
    float previous_water_level_m_;
    uint64_t previous_sample_ms_;
    uint32_t sequence_counter_;

    float read_water_level_sensor();
    float read_barometric_pressure();
    float read_soil_saturation();
    float read_battery_voltage();
};

} // namespace Sentinel
