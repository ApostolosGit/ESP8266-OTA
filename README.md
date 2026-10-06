# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.05**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- Network Debug explains Wi-Fi status, recorded disconnect reason, AP startup and MQTT client result in words.
- Current operating mode is shown separately: AP-only intentionally pauses router Wi-Fi/MQTT, and previous MQTT results are clearly labelled.
- DNS shows whether a lookup ran, so AP-only zero values are not presented as a lookup failure. TLS code zero says no TLS error was recorded.
- Descriptions and diagnostic formatting templates stay in flash; explicit branches avoid RAM lookup tables. No new text buffers are allocated.
- JSY-MK333 + SSD1309 static RAM usage is 1936 bytes lower than v4.04, verified from core 2.7.2 build totals.
- Host checks cover the reported AP-only snapshot, recovery, incomplete settings, retries, Wi-Fi reasons and broker access rejection.
- HTTP responses drain each 64-byte COPY write before queuing the next slice, limiting outstanding TCP heap use while MQTT/TLS is connected.
- Streaming responses have a four-second budget and bounded ACK waits. Cancelled or failed writes close promptly with an explicit positive timeout.
- Root, setup, debug, AP login, error/action and not-found handlers close their accepted connection on every exit.
- Low-memory root requests return HTTP 503 and rapid reloads return HTTP 429 with Retry-After and heap diagnostics, replacing the empty HTTP 204 used in v4.03.
- Normal writes require 1,024 bytes free heap and a 256-byte free block. Smaller 32-byte emergency replies report memory pressure when resources permit; critically depleted clients are closed without further writes.
- MQTT diagnostics report root requests, rapid reloads, memory-busy responses, write aborts and explicit socket closes.
- Automatic full-page refresh remains disabled. MQTT reconnection and confirmed Restart ESP from app v2.12 remain available.
- Actual extracted HTTP helpers/root passed 2,000 load/refresh pairs per meter with simulated COPY allocation/ACK release, low memory, 40 ms ACK latency, cancelled clients, short writes, ACK timeout, deadline and millis rollover.
- AP-only PIN, 49 deterministic startup/network/restart checks and signed DEH-history checks passed.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds on ESP8266 core 2.7.2 passed.
- These are build/host checks; device behavior must be confirmed after installation.
- DEH indication anchors, delayed DEH measurements and signed Diff = Estimate now - Latest DEH remain available.
- Build source: `2621d6623ef1cd3c8291d64d2134f39f4d7e3e07`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37425142608

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.


