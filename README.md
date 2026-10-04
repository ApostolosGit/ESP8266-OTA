# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **3.14**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- Credentials: loaded from LittleFS; missing/invalid saved settings open the local setup portal.
- With valid saved settings, Wi-Fi outages keep local metering running with periodic retries.
- FLASH opens/closes setup AP during normal operation; an initialized meter keeps measuring in manual AP.
- OLED/RTC startup checkpoints identify the next pending operation.
- Exact near-now E.K. readings (inclusive ±5 minutes with full date/time) correct the estimate only. Frozen same-period comparison is stored before correction. Only the latest active E.K. may be deleted; its removal restores the previous basis plus intervening consumption.
- Setup AP address: 192.168.1.80.
- Transport: HTTPS range download triggered through MQTT.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds and firmware host checks passed.
- Build source: `545a552650a4f510b06c8beb36b85ec2ab78af33`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37228124988

## Manifests

MQTT.app v2.07+ selects by meter type:

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Additional SH1106 manifests are `manifest-jsy-sh1106.txt` and `manifest-dds-sh1106.txt`; existing app routing remains the SSD1309 profiles.

Every manifest contains the exact binary filename, byte size and MD5. Previous binaries remain available.
Publishing these files does not install firmware on devices; updates start only when requested.
