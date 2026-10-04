# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: 3.13
- Targets:
  - JSY-MK333 + SSD1309 (OLED2)
  - DDS238 + SSD1309 (OLED2)
- Credentials: loaded from LittleFS; if missing or unusable, the firmware opens the local setup portal
- Setup AP address: 192.168.1.80
- Transport: HTTPS range download triggered through MQTT
- CI gate: JSY-MK333 + OLED2 and DDS238 + OLED2 must both pass

Current manifests:

- `manifest-jsy.txt`
- `manifest-dds.txt`
- `manifest.txt` remains the JSY manifest for backward compatibility with older MQTT.app versions.

MQTT.app v2.07+ selects the correct manifest automatically by meter type.
