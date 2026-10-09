# ESP8266 OTA

Current firmware: **5.57**. App: **5.56**.

- v5.57 targets the long-run JSY case where router Wi-Fi remains associated but MQTT reaches state -2 and both MQTT access and the local HTTP page become unavailable.
- The frequent MQTT update-request parser is now allocation-free, avoiding repeated Arduino String heap churn during app auto-refresh.
- Failed state publications stay pending but retry with 5/10/30 second backoff instead of continuously retrying every 1.5 seconds under network or memory pressure.
- After a previously healthy MQTT session, repeated state -2 failures are tracked. Under clear local heap/TLS pressure, four failures schedule a network-stack self-heal; ordinary external broker/Internet failures use a more conservative threshold.
- Self-heal closes BearSSL/TCP and the HTTP listener, briefly cycles station Wi-Fi, reapplies the saved/static network profile, and restarts MQTT + web services without rebooting the ESP or resetting energy accounting.
- Network Debug reports the state -2 streak, network self-heal count and current MQTT update retry delay.
- Existing v5.56 request coalescing, V5 history, DEH logic, meter health, unique MAC-based MQTT IDs, AP PIN, OTA and web safeguards remain in place.
- All four firmware CI builds passed: DDS238/JSY-MK333 × SH1106/SSD1309.
- Build source: `2918768beb1f320a6c5cdfe045ca7e3362122d77`.
- Build run: https://github.com/ApostolosGit/ESP8266/actions/runs/37942269782

## Manifests

- `manifest-jsy.txt`: JSY-MK333 + SSD1309.
- `manifest-dds.txt`: DDS238 + SSD1309.
- `manifest-jsy-sh1106.txt`: JSY-MK333 + SH1106.
- `manifest-dds-sh1106.txt`: DDS238 + SH1106.
- `manifest.txt`: JSY + SSD1309 compatibility alias.

Every manifest contains the exact binary filename, byte size and MD5.
Previous binaries remain available. Publishing these files does not install firmware on devices; updates start only when requested.
