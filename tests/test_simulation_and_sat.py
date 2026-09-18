import requests

BASE_URL = "http://localhost:3000/api/v1"

def test_environments():
    print("--- Testing Environment Switching & Scenarios ---")
    envs = ["INDUSTRIAL", "INDOOR", "NATURAL", "URBAN", "INFRASTRUCTURE", "REMOTE"]
    for env in envs:
        # Switch environment
        r = requests.get(f"{BASE_URL}/environment/switch/{env}")
        assert r.status_code == 200, f"Failed switch to {env}: {r.text}"
        data = r.json()
        print(f"Switched to {env}: {data['name']} ({len(data['sensors'])} sensors)")

        # Trigger scenarios
        for scen in ["NORMAL", "WARNING", "CRITICAL"]:
            sr = requests.post(f"{BASE_URL}/environment/scenario", json={"environment": env, "scenario": scen})
            assert sr.status_code == 200, f"Failed scenario {scen} for {env}: {sr.text}"
            sdata = sr.json()
            print(f"  -> Scenario {scen}: Risk={sdata['risk_level']} ({sdata['risk_score']}) | Siren={sdata['actuators']['siren_db']}dB | Relay={sdata['actuators']['motor_relay']}")

def test_satellite():
    print("\n--- Testing Open-Source Satellite Backend ---")
    # Status
    r = requests.get(f"{BASE_URL}/satellite/status")
    assert r.status_code == 200, f"Satellite status error: {r.text}"
    status = r.json()
    print(f"Station: {status['station_id']} | Status: {status['server_status']} | Target: {status['active_satellite']}")
    print(f"Rotor: Az={status['rotor_azimuth_deg']}°, El={status['rotor_elevation_deg']}° | Doppler={status['doppler_shift_khz']} kHz")

    # Passes
    r = requests.get(f"{BASE_URL}/satellite/passes")
    assert r.status_code == 200
    passes = r.json()
    sat_name = passes[0].get('satellite_name') or passes[0].get('satellite')
    print(f"Upcoming Passes: {len(passes)} passes found (Next: {sat_name})")

    # Downlink Telemetry
    r = requests.get(f"{BASE_URL}/satellite/telemetry")
    assert r.status_code == 200
    telems = r.json()
    print(f"Downlink Frames: {len(telems)} frames logged (Latest: Frame #{telems[0]['frame_id']}, SNR={telems[0]['snr_db']}dB)")

    # Emergency Space-Burst Uplink
    r = requests.post(f"{BASE_URL}/satellite/uplink", json={
        "message": "[PRIORITY 1] TEESTA RIVER WATER SURGE +3.2M EMERGENCY TRIP",
        "satellite": "SATNOGS-LEO-01",
        "emergency_override": True
    })
    assert r.status_code == 200
    uplink = r.json()
    print(f"Uplink Transmitted: CRC16={uplink['crc16']} | Status={uplink['status']} | Network={uplink['network']}")

    # Configure custom backend server
    r = requests.post(f"{BASE_URL}/satellite/config", json={
        "backend_server_url": "https://network.satnogs.org/api"
    })
    assert r.status_code == 200
    print(f"Config updated: {r.json()['status']}")

if __name__ == "__main__":
    test_environments()
    test_satellite()
    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
