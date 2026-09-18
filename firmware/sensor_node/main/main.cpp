/**
 * @file main.cpp
 * @brief Sentinel-X Autonomous ESP32-S3 Disaster Sensor Node Entrypoint
 * 
 * Target: ESP32-S3 (Dual Xtensa LX7 @ 240MHz, 512KB SRAM, 8MB Octal Flash)
 * Framework: ESP-IDF v5.x / FreeRTOS
 * 
 * CORE BEHAVIOR:
 * 1. Periodically samples multi-parameter hydrological & weather sensors (1.0 Hz).
 * 2. Evaluates local kinematic bounds (&Delta;h/&Delta;t, physical plausibility).
 * 3. Evaluates local safety: RASPBERRY PI FAILURE != SAFETY FAILURE.
 *    Actuates local acoustic siren relay directly if threshold breached.
 * 4. Serializes compact binary and JSON telemetry frames.
 * 5. Transmits to Raspberry Pi 5 Edge Gateway via UART / ESP-NOW.
 */

#include "sensor_manager.h"
#include "safety_controller.h"
#include "telemetry.h"
#include "node_identity.h"
#include "fault_manager.h"

#include <cstdio>
#include <cstring>

#if defined(ESP_PLATFORM)
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"
#include "esp_log.h"
static const char* TAG = "SentinelMain";
#else
#include <thread>
#include <chrono>
#endif

using namespace Sentinel;

static SensorManager s_sensor_mgr;
static SafetyController s_safety_ctrl;

void sensor_telemetry_task(void* pvParameters) {
    char json_buffer[512];
    uint8_t binary_buffer[sizeof(CompactTelemetryFrame)];

    printf("============================================================\n");
    printf("SENTINEL-X ESP32-S3 SENSOR NODE FIRMWARE v2.4.1\n");
    printf("Node ID: %s | Core Principle: Local Autonomy Survives Gateway Loss\n", NodeIdentity::get_node_id());
    printf("============================================================\n");

    while (true) {
        // 1. Feed task watchdog
        FaultManager::feed_watchdog();

        // 2. Sample all physical sensors
        s_sensor_mgr.sample_all();
        const SensorReading& reading = s_sensor_mgr.get_latest_reading();

        // 3. Autonomous local safety check (Survives RPi 5 failure!)
        SafetyState safety_state = s_safety_ctrl.evaluate(reading);

        // 4. Serialize telemetry frames
        size_t json_len = TelemetrySerializer::to_json(reading, (uint8_t)safety_state, json_buffer, sizeof(json_buffer));
        size_t bin_len = TelemetrySerializer::to_compact_binary(reading, (uint8_t)safety_state, binary_buffer, sizeof(binary_buffer));

        // 5. Output telemetry packet over UART/Bus to Edge Gateway
        printf("[TELEMETRY TX #%u] Stage: %.2fm | Rate: %+.2fm/m | Baro: %.1fhPa | Sat: %.0f%% | Bat: %u%% | Safety: %u | Len: %zu B\n",
               (unsigned int)reading.sequence_num, reading.water_level_m, reading.rate_of_rise_m_min,
               reading.baro_pressure_hpa, reading.soil_saturation_pct, reading.battery_pct,
               (unsigned int)safety_state, bin_len);

        // 6. Sleep for 1000ms (1.0 Hz nominal rate)
#if defined(ESP_PLATFORM)
        vTaskDelay(pdMS_TO_TICKS(1000));
#else
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
#endif
    }
}

#if defined(ESP_PLATFORM)
extern "C" void app_main(void) {
    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize subsystems
    NodeIdentity::init();
    FaultManager::init();
    s_sensor_mgr.init();
    s_safety_ctrl.init();

    // Spawn high-priority telemetry FreeRTOS task
    xTaskCreatePinnedToCore(
        sensor_telemetry_task,
        "telemetry_task",
        4096,
        NULL,
        5, // Priority
        NULL,
        1  // Core 1
    );
}
#else
// Desktop simulation entry point (e.g. for CI / unit test runner)
int main() {
    NodeIdentity::init();
    FaultManager::init();
    s_sensor_mgr.init();
    s_safety_ctrl.init();
    sensor_telemetry_task(NULL);
    return 0;
}
#endif
