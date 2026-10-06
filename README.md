# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.06**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- Credentials are staged, flushed/closed and read-back verified before atomic LittleFS replacement. The previous record remains intact on staged write/read-back/rename errors.
- Wi-Fi startup no longer requires complete MQTT login fields. Broker rejection keeps Wi-Fi, HTTP and local metering active; saved credentials are retained.
- Empty password fields retain existing saved passwords; save success and restart follow a verified commit.
- Main-page readings update every five seconds through a small live fragment; no whole-page navigation, concurrent fetches or updates to hidden pages.
- Requests have a timeout and incomplete/busy responses preserve the previous measurements and retry.
- ESP8266 local date/time appears at the very bottom and is updated from the device response. Unsynchronized time is shown as --.
- Manual Refresh/retry text, the IDE_OTA/mDNS footer note and redundant main-page IP line are removed.
- Existing AP-only PIN, Network Debug descriptions, bounded HTTP COPY writes and network reconnection behavior remain available.
- Host checks cover actual credential save/load across simulated reboot, optional/bad MQTT fields, blank-password retention, PIN guard and staged write/read-back/rename faults.
- 51 startup/network/restart checks include MQTT rejection codes 4/5 preserving Wi-Fi/HTTP, and HTTP checks run 2,000 load/refresh pairs per meter.
- The emitted browser script passes cadence, timeout/retry, hidden-page pause, complete-fragment, single in-flight request and device-clock update checks.
- AP PIN and signed DEH accounting checks passed.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds on ESP8266 core 2.7.2 passed.
- Host/build checks do not independently reproduce hardware symptoms; device behavior needs confirmation after installation.
- Build source: `528c51e158805f6645c868fc6ef6cf4b7e5dd7bd`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37426943953

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing files does not install firmware on devices; updates start only when requested.

