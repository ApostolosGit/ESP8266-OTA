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

## Ventilation 1.08 — public OTA (compiled, hardware OTA unverified)

The newest public Ventilation application-only OTA file is [Ventilation_ESP8266_V1_08.bin](./Ventilation_ESP8266_V1_08.bin), 557,280 bytes (MD5 `6b52618d7c1d69b5dce12156f45ff050`; SHA256 `7d79f4bdd12489e3dbb521cd09c379876b2287fe1d085cb99394a2521d994391`). The public [manifest-ventilation.txt](./manifest-ventilation.txt) now points to **1.08** for normal opt-in MQTT.app OTA checks. Source: [Ventilation 1.08 private compiled release](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.08-test.27).

Network Debug, Network Setup with credential retention, Wi-Fi/MQTT/RSSI/heap status, and confirmed OTA-only Recovery follow the EnergyMeter ESP8266 v5.58 model. Ventilation STA and recovery AP are **192.168.1.81**; EnergyMeter ESP8266 is **192.168.1.80**; Boiler ESP32-C3 is **192.168.1.82**. The fan is forced OFF during OTA-only Recovery.

**Important:** Published as an opt-in OTA version after reproducible compilation and SHA/MD5 verification, **NOT** validated by a live MQTT OTA update or installed ventilation hardware. Do not initiate OTA unattended, with unsafe operating conditions, or without a tested on-site recovery path. Existing relay behavior has not been physically retested. No background or automatic device update is initiated by this repository commit. TLS authenticity remains unverified in the deployed firmware; MD5 alone is not a security signature.

## Separate Ventilation firmware — historical OTA test information

**Never flash Ventilation firmware to DDS238 or JSY meters, and never use EnergyMeter firmware on Ventilation.**

- Ventilation manifest: `manifest-ventilation.txt` (requires `meter=VENTILATION`).
- Historical Ventilation binary: `Ventilation_ESP8266_V1_05.bin` — 542,960 bytes, firmware **1.05**. The active manifest now points to v1.08.
- EnergyMeter binaries retain their existing `EnergyMeter_DDS238_*` and `EnergyMeter_JSY_*` names and existing DDS/JSY manifests, without modification.
- All manifests/binaries are in this repository root because the installed Ventilation v1.04 downloader has a **strict URL allowlist** requiring `https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/Ventilation_ESP8266_V...bin`. Moving firmware into another folder would be rejected by that existing installed firmware.
- Ventilation v1.05 is **TEST ONLY**; exact bytes copied from the private, compiled and checksum-verified [`ventilation-v1.05-test.16`](https://github.com/ApostolosGit/ESP8266-Ventilation/releases/tag/ventilation-v1.05-test.16). Not verified by an actual MQTT OTA on hardware.
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`.
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`.
- **No automatic remote installation.** The user must intentionally initiate and confirm OTA in MQTT.app, then provide their setup PIN.
- **Hardware risk:** no USB access and no bootloader A/B rollback; OTA failure could lose access. Remote HTTPS OTA implementation has not been validated in the deployed environment. Do not flash on safety-critical powered loads unattended.
