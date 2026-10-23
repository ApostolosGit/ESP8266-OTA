# Ventilation v1.05 — TEST OTA IMAGE (NO HARDWARE ROLLBACK)

**Test only; not validated end-to-end on the installed ESP8266.**

- Binary: `Ventilation_ESP8266_V1_05.bin` (542960 bytes)
- Manifest: `manifest-ventilation.txt`, only for `meter=VENTILATION`
- MD5: `9dd7b939e0930dc68160a11a1b073e2e`
- SHA256: `935e6d6759b6677b1384617c2e4419f28f5be9c1f1bc2b9f320c3151b790eb5c`
- Exact verified build: private GitHub Release `ventilation-v1.05-test.16`

**No automatic flash;** publish/update availability only. Run a supervised manual test with physical Wi-Fi access and stable power.
CAUTION: On v1.04 the OTA downloader requires enough free contiguous RAM for TLS, which has not been confirmed on the user's installed device; it may refuse to proceed even if the manifest is valid. There is no USB recovery or automatic boot rollback.
