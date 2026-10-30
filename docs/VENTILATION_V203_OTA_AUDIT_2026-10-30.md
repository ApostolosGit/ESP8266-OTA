# Ventilation ESP8266 V2.03 — OTA compatibility and safety review

**Review date:** 2026-10-30  
**Status:** **TEST CANDIDATE ONLY — NOT APPROVED FOR INSTALLED/PRODUCTION OTA**  
**Production manifest:** stays on **V2.02** (do not automatically change it).

## Candidate and immutable evidence

- Source: private `ApostolosGit/ESP8266-Ventilation`, `Ventilation_ESP8266_V2_03.ino`.
  Source is not copied into this public repository.
- Builder: [successful public run #41081881950](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41081881950).
- Release: [public V2.03 TEST-only prerelease](https://github.com/ApostolosGit/ESP8266-OTA.bin/releases/tag/ventilation-v2.03-test-41081881950-1).
- Artifact: `Ventilation_ESP8266_V2_03_TEST_ONLY.bin`, **587952 bytes**.
- SHA-256: `5f28d1247425522a5b0c9785115cae8873902494481d835d8d287f6e0625a35d`.
- MD5: `bfe43da5608f113b79519d65563c6da6`.
- Board build: `esp8266:esp8266:nodemcuv2`, ESP8266 core `2.7.2`.
- The public build copy includes only a C++ forward declaration necessary for Arduino
  auto-prototype generation. Original private `.ino` is not changed.

## Checks completed

1. **Build PASS.** Arduino CLI produced an ESP8266 application BIN with header `0xE9`.
2. **Release integrity PASS.** Full 587952-byte public download matches release MD5 and SHA-256.
3. **HTTP byte-range PASS.** Requests for bytes `0-4095` and `583856-587951`
   each returned **206 Partial Content**, exact 4096-byte payloads and correct
   `Content-Range`, with **one HTTP redirect** to GitHub's release-assets CDN.
   Evidence: [validation run #41083294111](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41083294111).
4. **OTA identifiers PASS (static review).** V2.02 and V2.03 both use OTA protocol
   **2** and profile `ventilation-3ds18b20-2dht11-none`. MQTT OTA command remains
   `ota_https_v2|<size>|<md5>|<https_url>|<profile>`.
5. **Actuator pre-OTA stop present (static review).** `applicationPrepareOta()`
   sets the fan OFF on GPIO12 before network/flash work. This requires real
   relay-polarity verification on the installed system.
6. **Size gate present (static review).** Incoming OTA checks reported
   `ESP.getFreeSketchSpace()` >= new image size.
7. **Low-memory gate present (static review).** OTA download checks
   available heap and contiguous block before attempting TLS.
8. **Fail-safe logic present (static review).** Two critical DS18B20 sensors can
   latch SafeMode after ten bad samples. A restart clears that RAM latch;
   this behavior must be verified in the field.

## Not verified — blockers before production

- **Actual installed ESP8266 flash/FS layout:** report actual
  `ESP.getFreeSketchSpace()`, configured/physical flash size; must fit
  **587952 bytes**.
- **Actual run-time TLS heap and fragmentation:** ensure free heap is at least
  **15000 bytes** and maximum contiguous block at least **9000 bytes** at OTA
  entry. Initial source checks are not live measurements.
- **Real ESP8266 HTTPClient/BearSSL end-to-end:** cloud requests successfully
  tested first and last ranges, but not all ~144 HTTP range fetches on
  the installed device; nor live `Update.end()` behavior.
- **Physical relay and recovery:** verify GPIO12 LOW = fan OFF, GPIO13
  speed output, active load disconnected for the first trial; verify
  behavior after reboot/power interruption and verify USB serial recovery.
- **SafeMode:** disconnect OUTSIDE / INSIDE independently in AUTO and MANUAL;
  ensure fan OFF, latch, and explicit three-valid-sample rearm.
  Disconnect MIDDLE and DHT11 independently; these should not latch
  critical SafeMode. Reboot behavior must be deliberately checked.
- **Security:** both MQTT and OTA TLS connections call `setInsecure()`
  (server certificate not verified). MD5 detects accidental/corrupt bytes
  but is **not** proof of firmware origin or signer authenticity. Restrict
  who can publish MQTT admin OTA commands and plan stronger verification
  before unattended/production rollouts.

## Controlled hardware test and promotion gate

1. Keep `manifest-ventilation.txt` pointing to **V2.02**.
2. On a bench ESP8266 with the **same flash layout and wiring**, disconnect
   the actual fan load. Confirm LOW really means relay OFF.
3. Observe free sketch space and TLS heap diagnostics. Confirm OTA download
   and flash can complete; confirm the device reports `firmware=2.03`,
   the expected profile and a working MQTT session.
4. Exercise SafeMode, manual control, relay/power-cycle behavior, Recovery,
   and verify existing LittleFS Wi-Fi/MQTT credentials survive OTA.
5. Only after successful documented hardware testing, separately approve
   a production `Ventilation_ESP8266_V2_03.bin` promotion and update of
   `manifest-ventilation.txt` with the exact size, MD5, SHA-256 and profile.

**No production flash, automatic OTA command, release promotion, or manifest
change is part of this review.**
