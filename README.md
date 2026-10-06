# ESP8266 OTA

Current firmware: **5.00**. App: **2.13**.

- New daily history begins with the first valid physical-meter reading after upgrading; old days are not reconstructed.
- Each day stores import/export separately for Z1, Z2 night and Z2 midday. Net charts use import minus export, including negative balances.
- Daily storage is bounded to 730 records of 80 bytes (58,400 bytes plus filesystem overhead). Current state uses two checksum-protected 112-byte banks, saved every 30 minutes and at transitions.
- The existing 45-day, 30-minute checkpoint history is retained. Charts retrieve at most 16 rows per MQTT page; no full-history RAM buffer is allocated.
- Partial days, uncertain gap allocation, physical counter resets and missing data are identified. Energy recovered after gaps longer than two hours is assigned to the return day and marked estimated.
- Network debug reports LittleFS total/used/free bytes, current RAM/largest block and boot minima while MQTT is connected. The app shows a connected-MQTT snapshot when receiving history.
- The daily ring preserves at least 400,000 bytes of flash headroom for existing checkpoint compaction and settings. Storage failures are reported; local meter operation continues.
- Existing Wi-Fi/MQTT recovery, AP-only web PIN, credential persistence and five-second web updates are preserved.
- Public binaries contain no Wi-Fi or MQTT login secrets. Broker host and port remain public defaults; saved credentials are read from LittleFS.
- Four firmware CI builds and extracted-function history/network/HTTP/DEH tests passed. Runtime free space/heap on the actual device is measured after installation.

Build source: `e616b6f1fded17f3ee28bb805b1d18d3aa519bd1`.
Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37479164605

Manifests: `manifest-jsy.txt` and `manifest-dds.txt` target SSD1309; `manifest-jsy-sh1106.txt` and `manifest-dds-sh1106.txt` target SH1106. `manifest.txt` aliases JSY + SSD1309. Each lists exact filename, size and MD5. Previous binaries remain available.

Publishing makes the firmware available to the app; it does not install it on devices.
