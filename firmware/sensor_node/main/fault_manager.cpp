/**
 * @file fault_manager.cpp
 * @brief Implementation of hardware watchdog & fault logging
 */

#include "fault_manager.h"
#include <cstdio>

#if defined(ESP_PLATFORM)
#include "esp_task_wdt.h"
#include "esp_log.h"
static const char* TAG = "FaultManager";
#endif

namespace Sentinel {

static uint32_t s_fault_count = 0;

bool FaultManager::init() {
#if defined(ESP_PLATFORM)
    esp_task_wdt_config_t wdt_config = {
        .timeout_ms = 10000,
        .idle_core_mask = (1 << 0) | (1 << 1),
        .trigger_panic = true
    };
    esp_task_wdt_init(&wdt_config);
    esp_task_wdt_add(NULL);
    ESP_LOGI(TAG, "Hardware Task Watchdog initialized (10s timeout)");
#endif
    return true;
}

void FaultManager::feed_watchdog() {
#if defined(ESP_PLATFORM)
    esp_task_wdt_reset();
#endif
}

void FaultManager::report_sensor_fault(uint8_t sensor_idx, const char* reason) {
    s_fault_count++;
#if defined(ESP_PLATFORM)
    ESP_LOGE(TAG, "SENSOR FAULT ISOLATED: Sensor #%u &bull; %s", sensor_idx, reason);
#else
    printf("[FAULT MANAGER] Sensor #%u isolated: %s\n", sensor_idx, reason);
#endif
}

uint32_t FaultManager::get_fault_count() {
    return s_fault_count;
}

} // namespace Sentinel
