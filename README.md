# ESP8266 OTA

Current EnergyMeter production firmware: **6.00**, for **SSD1309**.

EnergyMeter 6.00 is the first application generated from
`ESP8266_common_platform` 1.00. One firmware image includes the common services,
EnergyMeter application, selected DDS238 or JSY-MK333 driver and SSD1309 display.
Source: [ESP8266_EnergyMeter commit `f7b90a8`](https://github.com/ApostolosGit/ESP8266_EnergyMeter/commit/f7b90a85d92cf642d30038ed8937b5d97075165d),
under `ESP8266_common_platform/`. Build date: **27/10/2026**.

The v5.58 accounting/storage formats and MQTT topics remain compatible. All six
platform/application/display builds and all five host suites passed, including
record-layout compatibility, offline/recovery behavior and OTA profile checks.
**Installation on a physical device has not yet been verified.**

## Update from MQTT.app

Use [MQTT.app](https://apostolosgit.github.io/dds238-app/) **5.80 or newer**.
Select the EnergyMeter device, check the available update, confirm the target
and enter the existing PIN. The ESP8266 downloads the image directly over HTTPS,
checks its size and MD5, writes firmware and restarts. Publication does not
initiate installation on a device.

- An installed 5.58/5.59 uses its existing OTA command for the first transition.
  Because that firmware does not report the display type, the app requires
  explicit confirmation that the device has **SSD1309**.
- Firmware 6.00 reports application, driver, display, profile, platform version
  and OTA protocol. Subsequent app updates use the profile-checked v2 command;
  incompatible profiles and the legacy OTA command are rejected by 6.00.
- Success requires a fresh message from the same device reporting the expected
  firmware and profile. The app displays update stages while MQTT is disconnected.

## Manifests and images

| Manifest | Target | Active version |
| --- | --- | --- |
| `manifest-dds.txt` | DDS238 + SSD1309 | **6.00** |
| `manifest-jsy.txt` | JSY-MK333 + SSD1309 | **6.00** |
| `manifest.txt` | Byte-identical alias of `manifest-jsy.txt` | **6.00** |
| `manifest-dds-sh1106.txt` | Historical DDS238 + SH1106 | 5.59 |
| `manifest-jsy-sh1106.txt` | Historical JSY-MK333 + SH1106 | 5.59 |

Only the two SSD1309 EnergyMeter images are published for 6.00. Existing SH1106
manifests and all historical binaries are retained unchanged. The platform-only
and no-OLED validation images are not production OTA targets.

| Profile | Binary | Bytes | MD5 |
| --- | --- | ---: | --- |
| DDS238 + SSD1309 | `EnergyMeter_DDS238_SSD1309_Ver6_00_f7b90a8.bin` | 596688 | `66c29a8cfb4a31f36bed34b45f53db27` |
| JSY-MK333 + SSD1309 | `EnergyMeter_JSY_MK333_SSD1309_Ver6_00_f7b90a8.bin` | 601776 | `d4d4c77a076af929a0746e9ab6c2877d` |

The 6.00 manifests include the exact binary size, MD5 and SHA256, generated
source SHA256, source commit, core/credential/transport fields and the full
application/driver/display profile. The `ota_protocol=2` field describes 6.00;
legacy firmware can still install that image using its existing command.
Binary filenames contain the source-commit suffix `f7b90a8` and do not
reuse earlier release URLs.

Run `python3 -m unittest discover -s tests -p 'test_verify_release.py'` for the
verifier's rejection/range tests and `python3 tests/verify_release.py` for local
manifests, profiles and image hashes. After publication,
`python3 tests/verify_release.py --remote` also checks public manifest bytes,
full binary downloads, and first/middle/final 4096-byte HTTP 206 ranges.

## Ventilation 2.01 — memory and network diagnostics fix

The public [manifest-ventilation.txt](./manifest-ventilation.txt) selects
[Ventilation_ESP8266_V2_01.bin](./Ventilation_ESP8266_V2_01.bin), **582,480 bytes**,
MD5 `4c6a9bdea36d57fa70e5527348039672`,
SHA256 `7de0eda99bce9c5c4773c58c8a731f1b8337ad109c74d6b81c97f0ad8b657052`.
Source: [Ventilation application and common platform, commit `c855782`](https://github.com/ApostolosGit/ESP8266_EnergyMeter/tree/c855782bbe6bc9359ea0846884328b71121bf512/ESP8266_common_platform).
The manifest records the exact source commit and generated-source SHA256.

Ventilation 2.01 uses **ESP8266_common_platform 1.02**, without OLED, at
**192.168.1.81** for both the local LAN page and setup/recovery AP. Sensor,
fan/speed, schedule and history behavior remain based on the supplied 1.07
application. Existing credential migration and history A/B formats are retained.

This release addresses two findings from the reported 2.00 MQTT failure:

- Minute-history RAM uses compact 1/80 °C samples, preserving DS18B20 resolution
  and persisted history formats. Compiled static RAM falls from **58,220** to
  **52,568 bytes**, freeing **5,652 bytes** for runtime networking/TLS.
- `/network-debug` no longer truncates after DNS because of its response
  buffer. `/mqtt-status` exposes heap/TLS status and distinguishes the last
  connection attempt from the current MQTT client state.

The earlier truncated diagnostics did not establish the physical device's
MQTT failure cause. Memory pressure and diagnostic visibility are improved;
actual MQTT reconnection and the new firmware still require device validation.

Use [MQTT.app](https://apostolosgit.github.io/dds238-app/) **5.81 or newer**
when the device has a working MQTT connection. Installed **1.04–1.xx** uses the
existing PIN-protected legacy command; devices running **2.xx** use the common
profile-checked `ota_https_v2` command. The exact target profile remains
`ventilation-3ds18b20-2dht11-none`. The app confirms success only after a fresh
health message from the same device reports the expected version and profile.

A 2.00 device that is offline in MQTT cannot receive an app OTA command.
Download and extract the [local LAN Recovery package](./Ventilation_ESP8266_V2_01_local_OTA.zip)
on a computer on the same LAN with Python 3 installed. From the extracted
folder run `python3 tools/local_ota.py --install` (Windows:
`py tools/local_ota.py --install`). The helper verifies the packaged image,
identifies the device at **192.168.1.81**, enters Recovery with the fan OFF,
uploads over the LAN and checks the new firmware report. USB is not required.
If the PC has several network interfaces, specify its LAN address with
`--host-ip`. Running the helper without `--install` only validates local files;
it does not contact the device. Publication does not start an installation.

The existing EnergyMeter manifests and all earlier binaries, including
[Ventilation 2.00](./Ventilation_ESP8266_V2_00.bin), remain unchanged.
`python3 tests/verify_release.py --remote` verifies both EnergyMeter and
Ventilation, including complete image bytes and first/middle/final 4096-byte
HTTP 206 ranges. A live hardware OTA installation has not been performed.

## Separate Ventilation firmware — historical OTA test information

**Never flash Ventilation firmware to DDS238 or JSY meters, and never use EnergyMeter firmware on Ventilation.**

- Ventilation manifest: `manifest-ventilation.txt` (requires `meter=VENTILATION`).
- Historical Ventilation binaries: `Ventilation_ESP8266_V1_05.bin` — 542,960 bytes, firmware **1.05**, and `Ventilation_ESP8266_V1_08.bin` — 557,280 bytes, firmware **1.08**. The active manifest now points to **2.01**.
- EnergyMeter binaries retain their existing `EnergyMeter_DDS238_*` and `EnergyMeter_JSY_*` names and existing DDS/JSY manifests, without modification.
- All manifests/binaries are in this repository root because the installed Ventilation v1.04 downloader has a **strict URL allowlist** requiring `https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/Ventilation_ESP8266_V...bin`. Moving firmware into another folder would be rejected by that existing installed firmware.
- Ventilation v1.05 is **TEST ONLY**; exact bytes copied from the private, compiled and checksum-verified [`ventilation-v1.05-test.16`](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.05-test.16). Not verified by an actual MQTT OTA on hardware.
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`.
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`.
- **No automatic remote installation.** The user must intentionally initiate and confirm OTA in MQTT.app, then provide their setup PIN.
- **Hardware risk:** no USB access and no bootloader A/B rollback; OTA failure could lose access. Remote HTTPS OTA implementation has not been validated in the deployed environment. Do not flash on safety-critical powered loads unattended.
