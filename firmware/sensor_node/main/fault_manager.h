/**
 * @file fault_manager.h
 * @brief Watchdog timer and sensor fault isolation for ESP32-S3 Node
 */

#pragma once

#include <cstdint>

namespace Sentinel {

class FaultManager {
public:
    static bool init();
    static void feed_watchdog();
    static void report_sensor_fault(uint8_t sensor_idx, const char* reason);
    static uint32_t get_fault_count();
};

} // namespace Sentinel
