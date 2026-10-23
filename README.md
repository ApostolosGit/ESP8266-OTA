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

## Separate Ventilation firmware — TEST OTA only

**Never flash Ventilation firmware to DDS238 or JSY meters, and never use EnergyMeter firmware on Ventilation.**

- Ventilation manifest: `manifest-ventilation.txt` (requires `meter=VENTILATION`).
- Ventilation binary: `Ventilation_ESP8266_V1_05.bin` — 542,960 bytes, firmware **1.05**.
- EnergyMeter binaries retain their existing `EnergyMeter_DDS238_*` and `EnergyMeter_JSY_*` names and existing DDS/JSY manifests, without modification.
- All manifests/binaries are in this repository root because the installed Ventilation v1.04 downloader has a **strict URL allowlist** requiring `https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/Ventilation_ESP8266_V...bin`. Moving firmware into another folder would be rejected by that existing installed firmware.
- Ventilation v1.05 is **TEST ONLY**; exact bytes copied from the private, compiled and checksum-verified [`ventilation-v1.05-test.16`](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.05-test.16). Not verified by an actual MQTT OTA on hardware.
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`.
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`.
- **No automatic remote installation.** The user must intentionally initiate and confirm OTA in MQTT.app, then provide their setup PIN.
- **Hardware risk:** no USB access and no bootloader A/B rollback; OTA failure could lose access. Remote HTTPS OTA implementation has not been validated in the deployed environment. Do not flash on safety-critical powered loads unattended.
