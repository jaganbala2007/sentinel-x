/**
 * @file telemetry.cpp
 * @brief Implementation of compact frame & JSON serialization
 */

#include "telemetry.h"
#include <cstdio>
#include <cstring>
#include <cmath>

namespace Sentinel {

uint16_t TelemetrySerializer::calculate_crc16(const uint8_t* data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021; // CCITT polynomial
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

size_t TelemetrySerializer::to_json(const SensorReading& reading, uint8_t safety_state, char* out_buf, size_t max_len) {
    return (size_t)snprintf(out_buf, max_len,
        "{\"node_id\":\"%s\",\"seq\":%u,\"ts\":%llu,\"stage_m\":%.2f,\"rate_m_min\":%.2f,"
        "\"baro_hpa\":%.1f,\"soil_pct\":%.1f,\"battery_pct\":%u,\"safety_state\":%u,\"conf\":%.2f}",
        reading.node_id,
        (unsigned int)reading.sequence_num,
        (unsigned long long)reading.timestamp_ms,
        reading.water_level_m,
        reading.rate_of_rise_m_min,
        reading.baro_pressure_hpa,
        reading.soil_saturation_pct,
        reading.battery_pct,
        safety_state,
        reading.confidence
    );
}

size_t TelemetrySerializer::to_compact_binary(const SensorReading& reading, uint8_t safety_state, uint8_t* out_buf, size_t max_len) {
    if (max_len < sizeof(CompactTelemetryFrame)) {
        return 0;
    }

    CompactTelemetryFrame frame;
    frame.preamble[0] = 0x53; // 'S'
    frame.preamble[1] = 0x58; // 'X'
    frame.version = 0x02;
    frame.node_num = 1; // Default NODE-01
    frame.sequence_num = reading.sequence_num;
    frame.timestamp_sec = (uint32_t)(reading.timestamp_ms / 1000);
    frame.water_level_cm = (uint16_t)std::round(reading.water_level_m * 100.0f);
    frame.rate_of_rise_mm_m = (int16_t)std::round(reading.rate_of_rise_m_min * 1000.0f);
    frame.baro_pressure_daPa = (uint16_t)std::round(reading.baro_pressure_hpa * 10.0f);
    frame.soil_sat_pct = (uint8_t)std::round(reading.soil_saturation_pct);
    frame.battery_pct = reading.battery_pct;
    frame.safety_state = safety_state;
    frame.confidence_pct = (uint8_t)std::round(reading.confidence * 100.0f);

    // Compute CRC over frame bytes excluding crc16 field itself
    frame.crc16 = calculate_crc16((const uint8_t*)&frame, sizeof(CompactTelemetryFrame) - 2);

    std::memcpy(out_buf, &frame, sizeof(CompactTelemetryFrame));
    return sizeof(CompactTelemetryFrame);
}

} // namespace Sentinel
