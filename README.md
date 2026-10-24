# ESP8266 OTA

Current firmware: **5.58**. App: **5.56**.

- v5.58 remains the active firmware release.
- The firmware is again kept as one Arduino `.ino` file for the simplest possible Arduino IDE workflow.
- Large logical sections are separated inside the source with clear `MODULE` / `END MODULE` banners and long `====` lines.
- The v5.57 long-run JSY MQTT/web recovery fix and the v5.58 cleanup remain unchanged.
- The single-file reorganization changed comments/source layout only. Main CI rebuilt all four variants and produced the same binary sizes and MD5 values as the published v5.58 binaries.
- No MQTT topic, stored record layout, DEH behavior, history format, physical-meter register map or OTA protocol changed.
- All four firmware CI builds passed: DDS238/JSY-MK333 × SH1106/SSD1309.
- Build source: `8676504387237094edad3eec05b8cdcd2cad3d96`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37992118550

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
The v5.59 binaries remain only as historical files; manifests now point to v5.58.

## Ventilation 1.08 — public OTA (compiled, hardware OTA unverified)

The newest public Ventilation application-only OTA file is [Ventilation_ESP8266_V1_08.bin](./Ventilation_ESP8266_V1_08.bin), 557,280 bytes (MD5 `6b52618d7c1d69b5dce12156f45ff050`; SHA256 `7d79f4bdd12489e3dbb521cd09c379876b2287fe1d085cb99394a2521d994391`). The public [manifest-ventilation.txt](./manifest-ventilation.txt) now points to **1.08** for normal opt-in MQTT.app OTA checks. Source: [Ventilation 1.08 private compiled release](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.08-test.27).

Network Debug, Network Setup with credential retention, Wi-Fi/MQTT/RSSI/heap status, and confirmed OTA-only Recovery follow the EnergyMeter ESP8266 v5.58 model. Ventilation STA and recovery AP are **192.168.1.81**; EnergyMeter ESP8266 is **192.168.1.80**; Boiler ESP32-C3 is **192.168.1.82**. The fan is forced OFF during OTA-only Recovery.

**Important:** Published as an opt-in OTA version after reproducible compilation and SHA/MD5 verification, **NOT** validated by a live MQTT OTA update or installed ventilation hardware. Do not initiate OTA unattended, with unsafe operating conditions, or without a tested on-site recovery path. Existing relay behavior has not been physically retested. No background or automatic device update is initiated by this repository commit. TLS authenticity remains unverified in the deployed firmware; MD5 alone is not a security signature.

## Separate Ventilation firmware — historical OTA test information

**Never flash Ventilation firmware to DDS238 or JSY meters, and never use EnergyMeter firmware on Ventilation.**

- Ventilation manifest: `manifest-ventilation.txt` (requires `meter=VENTILATION`).
- Historical Ventilation binary: `Ventilation_ESP8266_V1_05.bin` — 542,960 bytes, firmware **1.05**. The active manifest now points to v1.08.
- EnergyMeter binaries retain their existing `EnergyMeter_DDS238_*` and `EnergyMeter_JSY_*` names and existing DDS/JSY manifests, without modification.
- All manifests/binaries are in this repository root because the installed Ventilation v1.04 downloader has a **strict URL allowlist** requiring `https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/Ventilation_ESP8266_V...bin`. Moving firmware into another folder would be rejected by that existing installed firmware.
- Ventilation v1.05 is **TEST ONLY**; exact bytes copied from the private, compiled and checksum-verified [`ventilation-v1.05-test.16`](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.05-test.16). Not verified by an actual MQTT OTA on hardware.
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`.
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`.
- **No automatic remote installation.** The user must intentionally initiate and confirm OTA in MQTT.app, then provide their setup PIN.
- **Hardware risk:** no USB access and no bootloader A/B rollback; OTA failure could lose access. Remote HTTPS OTA implementation has not been validated in the deployed environment. Do not flash on safety-critical powered loads unattended.
