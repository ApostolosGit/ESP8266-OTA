# ESP8266 OTA

Current firmware: **5.59**. App: **5.56**.

- v5.59 reorganizes the monolithic firmware into focused Arduino src/ modules while preserving executable behavior.
- Main .ino now keeps configuration, shared state/types, setup() and loop().
- Implementations are split into storage/accounting, DDS238 driver, JSY driver, MQTT, meter display, local web, utility/OTA and recovery/network modules.
- The modules are header-only textual includes so the firmware remains a single translation unit; global ownership, persisted binary layouts, MQTT topics and meter behavior are unchanged.
- CI includes a source-equivalence test proving the expanded v5.59 executable code matches v5.58 after normalizing only the version bump and required forward declaration.
- Existing v5.57 long-run JSY MQTT/web self-heal and v5.58 cleanup remain unchanged.
- All four firmware CI builds passed: DDS238/JSY-MK333 × SH1106/SSD1309.
- Build source: `dcbcfa70fa64ca8e5be951a6f259d0777ff4d8e3`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37989126884

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.
