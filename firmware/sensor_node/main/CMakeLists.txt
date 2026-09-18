idf_component_register(
    SRCS 
        "main.cpp"
        "sensor_manager.cpp"
        "safety_controller.cpp"
        "telemetry.cpp"
        "node_identity.cpp"
        "fault_manager.cpp"
    INCLUDE_DIRS "."
    REQUIRES 
        "freertos" 
        "esp_timer" 
        "driver" 
        "esp_hw_support" 
        "nvs_flash" 
        "mbedtls"
)
