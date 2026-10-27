# ESP8266 OTA

Current EnergyMeter firmware: **5.59**.

- v5.59 is the active EnergyMeter firmware release, built from [source commit `0c874d3`](https://github.com/ApostolosGit/ESP8266_EnergyMeter/commit/0c874d36207835b387a14d83a544d9016f882171).
- The firmware remains one Arduino `.ino` file. This release removes write-only boot-memory diagnostics, redundant power-factor state, unused headers and obsolete build/test tooling.
- MQTT topics, stored V3/V5 record layouts, DEH behavior, physical-meter registers and the HTTPS range OTA protocol remain compatible with v5.58.
- All four local NodeMCU builds and all four current host-test commands passed before publication: DDS238/JSY-MK333 × SH1106/SSD1309, ESP8266 core 2.7.2.
- Build source: `0c874d36207835b387a14d83a544d9016f882171`; firmware build date: `27/10/2026`.
- The new binaries use the source-commit suffix `_0c874d3` to distinguish them from the historical, withdrawn v5.59 binaries and avoid reusing their download URLs.

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

The current [app](https://github.com/ApostolosGit/dds238-app) selects
`manifest-dds.txt` or `manifest-jsy.txt`, both for SSD1309. The SH1106 manifests
are published separately for clients that explicitly select that display profile.

Every EnergyMeter manifest contains version `5.59`, the exact binary filename,
byte size and MD5, meter/OLED profile, core version and source build commit.
The alias `manifest.txt` is byte-identical to `manifest-jsy.txt`.

| Profile | Binary | Bytes | MD5 |
| --- | --- | ---: | --- |
| DDS238 + SH1106 | `EnergyMeter_DDS238_SH1106_Ver5_59_0c874d3.bin` | 595712 | `4701d8addf73ca73caea68641f689258` |
| DDS238 + SSD1309 | `EnergyMeter_DDS238_SSD1309_Ver5_59_0c874d3.bin` | 595632 | `8216f19b6ea96f8ae33586c00f20fe55` |
| JSY-MK333 + SH1106 | `EnergyMeter_JSY_MK333_SH1106_Ver5_59_0c874d3.bin` | 600640 | `6497c71b3f08cf5ec7b0ebe3ba7829c6` |
| JSY-MK333 + SSD1309 | `EnergyMeter_JSY_MK333_SSD1309_Ver5_59_0c874d3.bin` | 600544 | `d070ee94cb1c814bdb54bf3c9bf32b0b` |

The original `_Ver5_59.bin` files remain historical and are not referenced by the
active manifests. The v5.57/v5.58 files are retained for history.

Run `python3 tests/verify_release.py` to check local profile routing, sizes and MD5.
After publication, run `python3 tests/verify_release.py --remote` to verify the
public manifests, full binary downloads and HTTP 206 byte-range responses used
by the firmware updater. Actual device installation is initiated from the app.

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
