# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.03**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- MQTT runtime recovery now survives router/Internet interruptions without ESP restart.
- A dead PubSubClient keepalive explicitly tears down stale BearSSL/TCP state.
- After a previously healthy MQTT connection drops, reconnect retries use 5 s, 10 s, then 30 s maximum.
- Runtime MQTT reconnects start with a clean TLS transport.
- Local web availability is restored under MQTT/TLS load by relaxing the v4.01 heap gate while retaining 64-byte guarded writes and the removal of automatic full-page refresh.
- v4.03 explicitly closes the root HTTP socket on success, failed/aborted writes and low-memory requests; a 350 ms guard safely ignores rapid reloads.
- Network Debug includes root request, ignored reload, write-abort and socket-close counters.
- MQTT.app v2.12 exposes Restart ESP with confirmation; firmware acknowledges the request, waits 1.2 seconds and restarts normally.
- 49 deterministic startup/network/restart checks, web/PIN checks and signed DEH-history checks passed before all four builds.
- v4.01 DEH semantics remain unchanged: latest DEH date is published, delayed DEH measurements are whole-kWh only, and Diff = Estimate now - Latest DEH.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds and host network recovery checks passed.
- Build source: `77f9905bcce35a5da828888861c3428f0ce77d91`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37413208927

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.
