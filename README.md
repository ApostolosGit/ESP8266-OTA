# ESP8266 OTA

Current firmware: **5.55**. App: **5.55**.

- V5 daily history begins with the first valid physical-meter reading; upgrading from 5.00 preserves existing LittleFS history, utility readings and credentials. Old days are not reconstructed.
- Each day stores import/export separately for Z1 and the two Z2 windows. App charts and tables show Z1, Z2 midday, Z2 night, using import minus export, including negative balances.
- Daily storage is bounded to 730 records of 80 bytes (58,400 bytes plus filesystem overhead). Current state uses two checksum-protected 112-byte banks, saved every 30 minutes and at transitions.
- The existing 45-day, 30-minute checkpoint history is retained. Charts retrieve at most 16 rows per MQTT page; no full-history RAM buffer is allocated.
- Partial days, uncertain gap allocation, physical counter resets and missing data are identified. Energy recovered after gaps longer than two hours is assigned to the return day and marked estimated.
- Network debug reports LittleFS total/used/free bytes, current RAM/largest block and boot minima while MQTT is connected. The app shows a connected-MQTT snapshot when receiving history.
- The daily ring preserves at least 400,000 bytes of flash headroom for existing checkpoint compaction and settings. Storage failures are reported; local meter operation continues.
- Existing Wi-Fi/MQTT recovery, AP-only web PIN, credential persistence and five-second web updates are covered by regression tests.
- Public binaries contain no Wi-Fi or MQTT login secrets. Broker host and port remain public defaults; saved credentials are read from LittleFS.
- Four firmware CI builds and extracted-function history/network/HTTP/DEH tests passed. Runtime free space/heap on the actual device is measured after installation.

- Each ESP uses a stable MQTT device ID with its full station MAC, for example `jsy_house-AABBCCDDEEFF`. Identical binaries at different sites have independent state, health, requests, admin commands and OTA hostname. The MQTT client ID was already hardware-specific; the shared topic ID caused collisions.
- A retained, small health message reports a missing/unresponsive physical DDS238 or JSY even when measurement publication is unavailable. It is sent on failure/recovery, MQTT reconnection and every 30 seconds. Failed physical reads do not advance energy history or counters.
- The app distinguishes an online ESP from a failed meter, hides old live measurements while a meter error is active, and isolates parsing/rendering/request timeouts by device. A failing device cannot stop discovery and refresh of other devices.
- App OTA timeout is three minutes. The app can confirm the firmware version from health without a physical sensor. First migration to a new MAC ID reports the newly detected ID without claiming a unique mapping from an old shared ID.
- IMPORTANT for the first migration: if two pre-5.01 ESPs share one old ID, remote commands on that old topic cannot select one physical ESP. Upgrade with only one of those old-ID ESPs connected at a time, or use local upload. After both run 5.01, they remain separately addressable. Old retained legacy IDs can remain visible until their old broker records are cleared; the new firmware does not clear a topic that another old ESP might still use.
- Successful app credentials are kept only in the current browser tab session and restored after reload; explicit disconnect or authentication rejection clears them. Browser password-manager entries are external to the app. New service-worker updates do not force navigation or reload of an active connection.

- App device actions are Settings, Charts, Update; Charts and Update share the accent background. Each chart bar displays its signed kWh value above it, including zero. Wide 7/30-day and hourly charts scroll horizontally with spacing based on number length.
- Chart rendering reuses Intl formatters, calculates each displayed bar once and suppresses repeated zero axis lines. The app removes uncalled helpers and obsolete metric-card styles, uses one automatic refresh interval per connection, and avoids automatic requests when the same device already has a pending response.
- Firmware removes unused write-only diagnostics and an obsolete reading comparator, shares the identical public network profile, and sizes each MQTT topic buffer from the selected profile, MAC and suffix. The MQTT client ID uses the full MAC-based device ID once; stable MQTT topics are retained across a 5.01 to 5.55 upgrade.
- Validation includes DDS/JSY with SH1106/SSD1309, accounting/day/DST/utility regressions, sensor failure/recovery and two hardware IDs, AP/PIN/credential/reconnect/HTTP stress checks, PWA/session handling and actual browser desktop/mobile chart layout.

Build source: `5462ee0f9887ab41676ddb1eb752ccf8664cca62`.
Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37680219112

Manifests: `manifest-jsy.txt` and `manifest-dds.txt` target SSD1309; `manifest-jsy-sh1106.txt` and `manifest-dds-sh1106.txt` target SH1106. `manifest.txt` aliases JSY + SSD1309. Each lists exact filename, size and MD5. Previous binaries remain available.

Publishing makes the firmware available to the app; it does not install it on devices.
