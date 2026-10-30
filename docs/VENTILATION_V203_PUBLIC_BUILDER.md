# Ventilation V2.03 public-cloud builder

The firmware source stays in **private** `ApostolosGit/ESP8266-Ventilation`.
The public `ApostolosGit/ESP8266-OTA.bin` repository runs an on-demand
Arduino CLI build on a standard GitHub-hosted Linux runner.

## One-time token setup (repository owner)

1. In GitHub **Settings > Developer settings > Personal access tokens >
   Fine-grained tokens**, generate a token (for example `VentilationSourceRead`).
2. **Resource owner:** `ApostolosGit`.
3. **Repository access:** **Only select repositories** →
   `ESP8266-Ventilation`.
4. **Repository permissions:** **Contents: Read-only** (Metadata read is automatic).
   Do not grant Actions, Administration or write permissions.
5. Copy the token once. **Never paste it into a chat, commit or issue.**
6. Open **ApostolosGit/ESP8266-OTA.bin > Settings > Secrets and variables >
   Actions > New repository secret**.
7. Add the secret with this exact name: `VENTILATION_SOURCE_READ_TOKEN`.
   Paste the token as the secret value. Rotate it when expired.

## Build

Open **Actions > Ventilation V2.03 - free public OTA builder > Run workflow**,
choose branch `main`. Option `publish_test_release`:

- `true`: after successful compile, create a **PUBLIC test prerelease**
  containing the application BIN and MD5/SHA256. No Actions artifact storage.
- `false`: compile/check only; no BIN is stored after the job ends.

The job runs only when started by `ApostolosGit` on `main`; it has no
automatic push/PR trigger. It fetches only
`Ventilation_ESP8266_V2_03.ino` from the private repo using the read-only
token, with `persist-credentials: false`. Only PUBLIC Arduino dependencies
are cached. The private sketch is never committed or uploaded as an artifact.

This does not update `manifest-ventilation.txt`. Production remains V2.02
until the TEST binary is reviewed and deliberately promoted. Do not remotely
flash installed ventilation equipment without power/relay safety tests and
a known-good physical recovery method; there is no guaranteed OTA rollback.

The resulting public BIN can reveal **embedded AP/Web PIN or other compiled
configuration** despite the sketch remaining private. Wi-Fi/MQTT credentials
are expected to remain in the device's LittleFS, not in the binary.

Note: anyone with write access to a public repository's main branch can
modify workflows. Restrict write access and protect `main`.
