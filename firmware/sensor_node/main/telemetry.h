/**
 * @file telemetry.h
 * @brief Telemetry serialization (JSON & Compact Binary Frame) for Sentinel-X
 */

#pragma once

#include "sensor_manager.h"
#include <cstdint>
#include <cstddef>

namespace Sentinel {

// Compact binary frame for HF Packet Radio & LoRa/Satellite transport
#pragma pack(push, 1)
struct CompactTelemetryFrame {
    uint8_t preamble[2];       // 0x53, 0x58 ('SX')
    uint8_t version;           // 0x02
    uint8_t node_num;          // 0x01..0x14
    uint32_t sequence_num;
    uint32_t timestamp_sec;
    uint16_t water_level_cm;   // Scale: cm (e.g. 241 = 2.41m)
    int16_t rate_of_rise_mm_m; // Scale: mm/min
    uint16_t baro_pressure_daPa;// DecaPascals
    uint8_t soil_sat_pct;
    uint8_t battery_pct;
    uint8_t safety_state;      // 0: Nominal, 1: Watch, 2: Warning, 3: Critical
    uint8_t confidence_pct;
    uint16_t crc16;            // CRC-16-CCITT
};
#pragma pack(pop)

class TelemetrySerializer {
public:
    static size_t to_json(const SensorReading& reading, uint8_t safety_state, char* out_buf, size_t max_len);
    static size_t to_compact_binary(const SensorReading& reading, uint8_t safety_state, uint8_t* out_buf, size_t max_len);
    static uint16_t calculate_crc16(const uint8_t* data, size_t len);
};

} // namespace Sentinel
