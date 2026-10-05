# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.01**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- Fixes the v3.19/v4.00 local web crash: the root page no longer reloads itself every 5 seconds, HTTP writes are guarded by free-heap/max-block checks, and flash-to-RAM write slices are reduced to 64 bytes.
- The local page now refreshes manually, avoiding repeated HTTP allocations while MQTT/TLS is active.
- MQTT state includes `utility_date`, the date of the latest DEH measurement used as **Τελευταία ΔΕΗ**.
- **Καταχώρηση Μέτρησης ΔΕΗ** accepts whole kWh only; **Καταχώρηση Ένδειξης Μετρητή ΔΕΗ** retains decimal precision.
- **Diff = Εκτίμηση τώρα − Τελευταία ΔΕΗ**, signed for photovoltaic export/import.
- Local latest/DEH display uses whole kWh.
- Setup links remain aligned as **Network Debug** and **Netword Setup**.
- Transport: HTTPS range download triggered through MQTT.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds and firmware host checks passed.
- Build source: `61d06fd72b5b9b3a7796878db2c07a5584cf9c62`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37349702593

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.
