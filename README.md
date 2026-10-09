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
