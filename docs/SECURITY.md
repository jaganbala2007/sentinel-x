# Sentinel-X Post-Quantum Security & Integrity Subsystem

**Standards Alignment:** NIST FIPS 203 (ML-KEM) & NIST FIPS 204 (ML-DSA)  
**Implementation State:** PQC PROTOTYPE / INTEGRATION INTERFACE  

---

## 1. Zero-Trust Security Architecture

Disaster sensing infrastructure deployed in public, unmonitored river basins faces severe tampering threats:
- Physical tapping or replay of emergency telemetry.
- Man-in-the-middle injection of fake flood warnings.
- Future quantum-assisted decryption of archived infrastructure telemetry ("Harvest Now, Decrypt Later").

---

## 2. Cryptographic Stack

```
[ESP32-S3 eFuse Hardware Root-of-Trust]
                   │
                   ▼
       [Ed25519 Signed Firmware Boot]
                   │
                   ▼
  [ML-KEM-768 Lattice Key Encapsulation]
                   │
                   ▼
   [AES-256-GCM Authenticated Session]
                   │
                   ▼
 [Monotonic Monadic Sequence Replay Protection]
```

### Protocol Details
- **Key Establishment:** ML-KEM-768 produces a 32-byte shared secret with 1088-byte ciphertext encapsulation.
- **Message Signatures:** ML-DSA-65 provides lattice-based digital signatures verifiable on low-power microcontrollers.
- **Replay Protection:** Monotonically increasing sequence counters paired with epoch timestamps reject replayed frames.
