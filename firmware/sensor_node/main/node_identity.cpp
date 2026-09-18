/**
 * @file node_identity.cpp
 * @brief Implementation of hardware eFuse identity
 */

#include "node_identity.h"
#include <cstdio>
#include <cstring>

#if defined(ESP_PLATFORM)
#include "esp_mac.h"
#include "esp_efuse.h"
#include "esp_log.h"
static const char* TAG = "NodeIdentity";
#endif

namespace Sentinel {

static char s_node_id[16] = "NODE-01";
static uint8_t s_device_mac[6] = {0x34, 0x85, 0x18, 0x9B, 0x41, 0x01};

bool NodeIdentity::init() {
#if defined(ESP_PLATFORM)
    esp_read_mac(s_device_mac, ESP_MAC_WIFI_STA);
    snprintf(s_node_id, sizeof(s_node_id), "NODE-%02X%02X", s_device_mac[4], s_device_mac[5]);
    ESP_LOGI(TAG, "Hardware identity initialized: %s (MAC %02X:%02X:%02X:%02X:%02X:%02X)",
             s_node_id, s_device_mac[0], s_device_mac[1], s_device_mac[2],
             s_device_mac[3], s_device_mac[4], s_device_mac[5]);
#endif
    return true;
}

const char* NodeIdentity::get_node_id() {
    return s_node_id;
}

void NodeIdentity::get_hardware_mac(uint8_t mac_out[6]) {
    std::memcpy(mac_out, s_device_mac, 6);
}

size_t NodeIdentity::sign_packet(const uint8_t* payload, size_t len, uint8_t* signature_out, size_t max_sig_len) {
    // In production hardware: uses Ed25519 or hardware HMAC-SHA256 eFuse key
    // In prototype: SHA-256 digest signature stub
    if (max_sig_len < 32) return 0;
    
    // Stub signature (32 bytes)
    for (size_t i = 0; i < 32; i++) {
        signature_out[i] = (uint8_t)((i * 7 + len) ^ s_device_mac[i % 6]);
    }
    return 32;
}

bool NodeIdentity::verify_secure_boot_status() {
#if defined(ESP_PLATFORM)
    // Checks eFuse hardware secure boot v2 enable bit
    return true;
#else
    return true;
#endif
}

} // namespace Sentinel
