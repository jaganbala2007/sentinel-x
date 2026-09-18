/**
 * @file node_identity.h
 * @brief Hardware Root-of-Trust and Device Identity for ESP32-S3 Node
 */

#pragma once

#include <cstdint>
#include <cstddef>

namespace Sentinel {

class NodeIdentity {
public:
    static bool init();
    static const char* get_node_id();
    static void get_hardware_mac(uint8_t mac_out[6]);
    static size_t sign_packet(const uint8_t* payload, size_t len, uint8_t* signature_out, size_t max_sig_len);
    static bool verify_secure_boot_status();
};

} // namespace Sentinel
