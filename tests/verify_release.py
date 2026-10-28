"""Validate OTA profile routing, image bytes and the public HTTP range path."""
import argparse
import hashlib
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/ApostolosGit/ESP8266-OTA/main/"
PROFILES = {
    "manifest-dds.txt": ("DDS238", "SSD1309"),
    "manifest-jsy.txt": ("JSY-MK333", "SSD1309"),
    "manifest-dds-sh1106.txt": ("DDS238", "SH1106"),
    "manifest-jsy-sh1106.txt": ("JSY-MK333", "SH1106"),
}
ACTIVE_VERSION = "6.00"
VENTILATION_VERSION = "2.02"
VENTILATION_PROFILE = "ventilation-3ds18b20-2dht11-none"
HISTORICAL_MANIFEST_SHA256 = {
    "manifest-dds-sh1106.txt": "ecf1b3f12587383008e100ea3676ee45c4ff3f66e3006a60d40cd8d15cd41fa2",
    "manifest-jsy-sh1106.txt": "8478564d85f63c3436dbf2078cfbb9df133a8423aed43f0ee073d3fa9378cb46",
}


def remote_bytes(path, nonce, byte_range=None, total_size=None):
    headers = {"Cache-Control": "no-cache", "Accept-Encoding": "identity"}
    if byte_range:
        start, end = byte_range
        headers["Range"] = f"bytes={start}-{end}"
        nonce += f"-{start}-{end}"
    request = urllib.request.Request(BASE + path + "?check=" + nonce, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        if byte_range:
            assert response.status == 206, f"{path}: HTTP {response.status}, expected 206"
            expected = f"bytes {start}-{end}/{total_size}"
            assert response.headers.get("Content-Range", "") == expected, f"{path}: wrong Content-Range"
        else:
            assert response.status == 200, f"{path}: HTTP {response.status}, expected 200"
        content = response.read()
        if byte_range:
            assert len(content) == end - start + 1, f"{path}: incomplete HTTP range"
        return content


def parse_manifest(content):
    fields = {}
    for line in content.decode().splitlines():
        if not line.strip():
            continue
        assert "=" in line, "Malformed manifest line"
        key, value = line.split("=", 1)
        assert key and key not in fields, f"Duplicate or empty manifest key: {key}"
        fields[key] = value
    return fields


def validate_manifest(manifest, content):
    profile = PROFILES[manifest]
    fields = parse_manifest(content)
    assert (fields["meter"], fields["oled"]) == profile, f"{manifest}: wrong hardware profile"
    path = fields["file"]
    assert re.fullmatch(r"[A-Za-z0-9._-]+\.bin", path), f"{manifest}: invalid binary filename"
    image = (ROOT / path).read_bytes()
    assert image and image[0] == 0xE9 and len(image) == int(fields["size"]), f"{path}: invalid image/size"
    assert hashlib.md5(image).hexdigest() == fields["md5"], f"{path}: MD5 mismatch"
    assert fields["core"] == "ESP8266-2.7.2"
    assert fields["credentials"] == "LittleFS-or-setup-portal"
    assert fields["transport"] == "https-range"
    if profile[1] == "SSD1309":
        assert fields["version"] == ACTIVE_VERSION, f"{manifest}: wrong active version"
        assert fields["application"] == "energymeter"
        assert fields["platform_version"] == "1.00"
        assert fields["driver"] == profile[0]
        expected = "energymeter-" + profile[0].lower() + "-ssd1309"
        assert fields["profile"] == expected, f"{manifest}: wrong OTA profile identity"
        assert fields["ota_protocol"] == "2"
        assert re.fullmatch(r"[0-9a-f]{40}", fields["build"]), f"{manifest}: invalid source commit"
        assert re.fullmatch(r"[0-9a-f]{64}", fields["source_sha256"]), f"{manifest}: invalid source digest"
        assert hashlib.sha256(image).hexdigest() == fields["sha256"], f"{path}: SHA256 mismatch"
    else:
        assert fields["version"] == "5.59", f"{manifest}: historical SH1106 version changed"
        assert hashlib.sha256(content).hexdigest() == HISTORICAL_MANIFEST_SHA256[manifest], f"{manifest}: historical manifest changed"
    return fields, image


def validate_ventilation_manifest(content):
    fields = parse_manifest(content)
    assert fields["version"] == VENTILATION_VERSION
    assert fields["file"] == "Ventilation_ESP8266_V2_02.bin", "Legacy Ventilation URL allowlist requires the exact versioned filename"
    for key, expected in {
        "meter": "VENTILATION", "application": "ventilation",
        "platform_version": "1.03", "driver": "DS18B20-DHT11",
        "oled": "NONE", "profile": VENTILATION_PROFILE, "ota_protocol": "2",
        "core": "ESP8266-2.7.2", "transport": "https-range",
        "credentials": "LittleFS-migration-or-setup-portal",
        "hardware_validation": "UNVERIFIED", "requires": "Ventilation-1.04+",
        "local_ip": "192.168.1.81",
    }.items():
        assert fields[key] == expected, f"Ventilation: invalid {key}"
    assert re.fullmatch(r"[0-9a-f]{40}", fields["build"]), "Ventilation: invalid source commit"
    assert re.fullmatch(r"[0-9a-f]{64}", fields["source_sha256"]), "Ventilation: invalid source digest"
    image = (ROOT / fields["file"]).read_bytes()
    assert image and image[0] == 0xE9 and len(image) == int(fields["size"]), "Ventilation: invalid image/size"
    assert hashlib.md5(image).hexdigest() == fields["md5"], "Ventilation: MD5 mismatch"
    assert hashlib.sha256(image).hexdigest() == fields["sha256"], "Ventilation: SHA256 mismatch"
    return fields, image


def verify_remote_image(manifest, content, fields, image):
    nonce = str(time.time_ns())
    path = fields["file"]
    assert remote_bytes(manifest, nonce) == content, manifest
    assert remote_bytes(path, nonce) == image, path
    length = 4096
    offsets = (0, (len(image) - length) // 2, len(image) - length)
    for start in offsets:
        end = start + length - 1
        actual = remote_bytes(path, nonce, (start, end), len(image))
        assert actual == image[start:end + 1], f"{path}: range {start}-{end} mismatch"


def check(remote=False):
    assert (ROOT / "manifest.txt").read_bytes() == (ROOT / "manifest-jsy.txt").read_bytes()
    active_builds = set()
    for manifest, profile in PROFILES.items():
        content = (ROOT / manifest).read_bytes()
        fields, image = validate_manifest(manifest, content)
        if profile[1] == "SSD1309":
            active_builds.add(fields["build"])
        path = fields["file"]
        if remote:
            verify_remote_image(manifest, content, fields, image)
        print(f"PASS {manifest}: {fields['version']} {profile} {len(image)} bytes", flush=True)
    assert len(active_builds) == 1, "SSD1309 profiles must use the same source commit"
    content = (ROOT / "manifest-ventilation.txt").read_bytes()
    fields, image = validate_ventilation_manifest(content)
    if remote:
        verify_remote_image("manifest-ventilation.txt", content, fields, image)
    print(f"PASS manifest-ventilation.txt: {fields['version']} {fields['profile']} {len(image)} bytes", flush=True)
    if remote:
        assert remote_bytes("manifest.txt", str(time.time_ns())) == (ROOT / "manifest.txt").read_bytes()
    print("REMOTE_OTA_MATCH_CHECKOUT=PASS" if remote else "LOCAL_OTA_CHECKS=PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", action="store_true")
    args = parser.parse_args()
    for attempt in range(6):
        try:
            check(args.remote)
            break
        except Exception:
            if not args.remote or attempt == 5:
                raise
            print("Waiting for public OTA files", flush=True)
            time.sleep(5)
