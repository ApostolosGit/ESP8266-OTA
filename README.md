# ESP8266 OTA

Current firmware: **5.58**. App: **5.56**.

- v5.58 is a documentation and safe-cleanup release on top of the v5.57 JSY MQTT/web stability fix.
- The firmware now starts with an architecture overview and documents the actual setup/loop execution model, memory rules, V3/V5 storage-schema compatibility, and current DEH indication/measurement semantics.
- Removed MQTT diagnostic variables that were written but never read, simplified an identical DDS/JSY MQTT buffer branch, and removed a normal-boot String allocation for IP formatting.
- The MQTT low-memory publish guard is unchanged logically; its temporary heap values now stay local to the publish operation.
- No MQTT topic, stored record layout, DEH behavior, history format, physical-meter register map or OTA protocol changed.
- JSY SSD1309 build decreased from 596,772 to 596,736 program bytes and from 48,420 to 48,416 global RAM bytes versus v5.57.
- All four firmware CI builds passed: DDS238/JSY-MK333 × SH1106/SSD1309.
- Build source: `dc7fd0c6b01e25e0dc3852a80bebeef1676386be`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37948374271

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.
