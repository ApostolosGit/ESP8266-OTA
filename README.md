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

## Ventilation 2.00 — common platform, no OLED

The public [manifest-ventilation.txt](./manifest-ventilation.txt) selects
[Ventilation_ESP8266_V2_00.bin](./Ventilation_ESP8266_V2_00.bin), **581,120 bytes**,
MD5 `cc1a5195bb81ddc586d8a501c687d73d`,
SHA256 `8ce9ba722cefe043631cfdf772bc07e31765dcf9572d999d59b7d729079b75f9`.
Source: [Ventilation application and common platform, commit `2723418`](https://github.com/ApostolosGit/ESP8266_EnergyMeter/tree/27234185ad18d3b0aa7264ca6ae5b5f6fb1c5420/ESP8266_common_platform).
The manifest records the exact source commit and generated-source SHA256.

Ventilation 2.00 combines **ESP8266_common_platform 1.01** with the sensors,
fan/speed controls, schedules and 24h/48h/30-day history from the supplied
Ventilation 1.07 source. This application has **no OLED**. Both its local LAN
page and setup/recovery AP use **192.168.1.81**; the old credential record is
validated and migrated, and existing history A/B formats remain compatible.
The fan remains OFF during OTA and Recovery.

Use [MQTT.app](https://apostolosgit.github.io/dds238-app/) **5.81 or newer**:
select Ventilation, confirm the offered 2.00 update and enter the existing PIN.
Installed **1.04–1.xx** uses the existing PIN-protected legacy OTA command for
this first migration. Devices already running **2.xx** use the common
profile-checked `ota_https_v2` command. Its exact profile is
`ventilation-3ds18b20-2dht11-none`; incompatible application/display/driver
profiles are rejected before installation.

The app waits for a fresh, non-retained health message from the same device
reporting the expected version and profile after the OTA disconnection.
Publication does not start an installation. The binary, profile, hashes and
range downloads were checked in software; a live hardware OTA installation
has not been performed.

The existing EnergyMeter manifests and all earlier binaries remain unchanged.
`python3 tests/verify_release.py --remote` verifies both EnergyMeter and
Ventilation, including complete image bytes and first/middle/final 4096-byte
HTTP 206 ranges.

## Separate Ventilation firmware — historical OTA test information

**Never flash Ventilation firmware to DDS238 or JSY meters, and never use EnergyMeter firmware on Ventilation.**

- Ventilation manifest: `manifest-ventilation.txt` (requires `meter=VENTILATION`).
- Historical Ventilation binaries: `Ventilation_ESP8266_V1_05.bin` — 542,960 bytes, firmware **1.05**, and `Ventilation_ESP8266_V1_08.bin` — 557,280 bytes, firmware **1.08**. The active manifest now points to **2.00**.
- EnergyMeter binaries retain their existing `EnergyMeter_DDS238_*` and `EnergyMeter_JSY_*` names and existing DDS/JSY manifests, without modification.
- All manifests/binaries are in this repository root because the installed Ventilation v1.04 downloader has a **strict URL allowlist** requiring `https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/Ventilation_ESP8266_V...bin`. Moving firmware into another folder would be rejected by that existing installed firmware.
- Ventilation v1.05 is **TEST ONLY**; exact bytes copied from the private, compiled and checksum-verified [`ventilation-v1.05-test.16`](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.05-test.16). Not verified by an actual MQTT OTA on hardware.
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`.
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`.
- **No automatic remote installation.** The user must intentionally initiate and confirm OTA in MQTT.app, then provide their setup PIN.
- **Hardware risk:** no USB access and no bootloader A/B rollback; OTA failure could lose access. Remote HTTPS OTA implementation has not been validated in the deployed environment. Do not flash on safety-critical powered loads unattended.
