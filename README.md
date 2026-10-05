# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.00**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- **Καταχώρηση Ένδειξης Μετρητή ΔΕΗ** uses the ESP's current local date/time and a fresh physical-meter read, stores the same-moment internal Import/Export anchor, drives **Εκτίμηση τώρα**, and is the only entry type used for accuracy/% evaluation.
- **Καταχώρηση Μέτρησης ΔΕΗ** stores the historical DEH measurement date/value as comparison-only data. It never remaps historical ESP counters and never replaces the estimate anchor.
- Of multiple DEH measurements, **Τελευταία ΔΕΗ** is the one with the most recent DEH measurement date/time.
- Live dashboard difference is **Diff = Εκτίμηση τώρα − Τελευταία ΔΕΗ** and may be positive or negative, including with photovoltaic export.
- Net energy uses Import − Export; directional anchors remain checksum-protected and persistent.
- Local dashboard keeps Network Debug and **Netword Setup** on the same line.
- Wi-Fi/MQTT login secrets are loaded from LittleFS; broker host/port are compiled public settings.
- Setup AP address: 192.168.1.80.
- Transport: HTTPS range download triggered through MQTT.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds and firmware host checks passed.
- Build source: `735e001c25bef1779fa2386f0a9325f1d4f84f95`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37343697457

## Manifests

MQTT.app selects by meter/OLED profile:

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5. Previous binaries remain available.
Publishing these files does not install firmware on devices; updates start only when requested.
