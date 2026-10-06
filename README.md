# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **4.04**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
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
- Build source: `6ca5d9fc9ab61caa5a4e9fd7c4c193087bab3384`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37422370613

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.

