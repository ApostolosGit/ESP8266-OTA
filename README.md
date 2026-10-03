# ESP8266 OTA

Public OTA hosting for EnergyMeter firmware.

## Current firmware

- Version: 3.00
- Target: JSY-MK333 + SH1106
- Size: 568752 bytes
- MD5: `b17912c84bc959b9457c23cd2ad5ee0b`
- Credentials: loaded from LittleFS; if missing or unusable, v3.00 opens the local setup portal
- Setup AP: temporary, password generated at runtime and shown on the OLED
- Transport: HTTPS range download triggered through MQTT

Firmware filename:

`EnergyMeter_JSY_MK333_SH1106_Ver3_00.bin`
