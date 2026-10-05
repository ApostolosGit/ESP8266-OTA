# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: **3.19**
- Default app targets: DDS238 + SSD1309 and JSY-MK333 + SSD1309.
- Additional binaries: DDS238 + SH1106 and JSY-MK333 + SH1106.
- Wi-Fi/MQTT login secrets: loaded from LittleFS; broker host/port: compiled public settings; missing/invalid saved settings open the local setup portal.
- With valid saved settings, Wi-Fi outages keep local metering running with periodic retries.
- FLASH opens/closes setup AP during normal operation; an initialized meter keeps measuring in manual AP.
- OLED/RTC startup checkpoints identify the next pending operation.
- Z/Z1/Z2 estimates use net import minus export and support photovoltaic export.
- New E.K. captures the ESP's current local time after a fresh meter read and freezes signed same-period comparison before correction. T.K. accepts a declared time or the 08:00–18:00 window.
- Full matched directional anchors are checksum-protected and persisted separately without changing V1 history storage. The app displays their net result beside the DEH reading.
- Editing an E.K. keeps the original source time; deleting the latest active E.K. restores the preceding basis and intervening net energy.
- Failures remain visible for at least 4 seconds while normal metering and reconnect work continue; queued categories and checksum-protected RTC replay preserve causes through redraws/restarts.
- Setup/recovery AP uses explicit .81–.100 DHCP leases; FLASH can open/retry setup in Recovery without leaving that mode. Recovery remains OTA-only.
- Setup AP Wi-Fi is open, with no network password. In AP mode only, all web pages/actions require PIN 12134; normal LAN web access keeps its existing behavior. PIN login uses a random browser session, valid for 15 minutes and reset when AP closes/reopens.
- Dashboard follows the supplied utility/measurements/network layout, with Phase–W–V–A–PF columns. Dashboard/setup/debug text uses 22 px; visible IDE OTA labels use IDE_OTA.
- Broker host/port are public compiled settings. Setup keeps only Wi-Fi SSID/password and MQTT username/password. Existing saved login secrets survive OTA; the compiled broker overrides older stored host/port.
- Clear credentials and Save & restart schedule an automatic restart after 1200 ms in LAN, AP, failed-AP and Recovery modes. Clearing removes only Wi-Fi/MQTT settings, so boot opens Setup AP; firmware OTA retains stored settings.
- Compact dashboard matches the new reference, with Z1/Z2 first, power beside Measurements, frequency/debug beside import/export, and setup/device footer.
- Setup AP address: 192.168.1.80.
- Transport: HTTPS range download triggered through MQTT.
- CI gate: all four DDS238/JSY × SH1106/SSD1309 builds and firmware host checks passed.
- Build source: `35903a2e427a81720594f02c6e2f66311bc705ff`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37331546660

## Manifests

MQTT.app v2.07+ selects by meter type:

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Additional SH1106 manifests are `manifest-jsy-sh1106.txt` and `manifest-dds-sh1106.txt`; existing app routing remains the SSD1309 profiles.

Every manifest contains the exact binary filename, byte size and MD5. Previous binaries remain available.
Publishing these files does not install firmware on devices; updates start only when requested.
