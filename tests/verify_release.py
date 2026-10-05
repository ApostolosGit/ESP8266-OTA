"""Validate OTA profile routing, image bytes and the public HTTP range path."""
import argparse
import hashlib
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


def remote_bytes(path, nonce, byte_range=None):
    headers = {"Cache-Control": "no-cache", "Accept-Encoding": "identity"}
    if byte_range:
        headers["Range"] = byte_range
    request = urllib.request.Request(BASE + path + "?check=" + nonce, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        if byte_range:
            assert response.status == 206, f"{path}: HTTP {response.status}, expected 206"
            assert response.headers.get("Content-Range", "").startswith("bytes 0-1023/")
        return response.read()


def check(remote=False):
    assert (ROOT / "manifest.txt").read_bytes() == (ROOT / "manifest-jsy.txt").read_bytes()
    versions = set()
    for manifest, profile in PROFILES.items():
        content = (ROOT / manifest).read_bytes()
        fields = dict(line.split("=", 1) for line in content.decode().splitlines() if "=" in line)
        assert (fields["meter"], fields["oled"]) == profile
        versions.add(fields["version"])
        path = fields["file"]
        assert Path(path).name == path and path.endswith(".bin")
        image = (ROOT / path).read_bytes()
        assert image[0] == 0xE9 and len(image) == int(fields["size"])
        assert hashlib.md5(image).hexdigest() == fields["md5"]
        assert fields["credentials"] == "LittleFS-or-setup-portal"
        assert fields["transport"] == "https-range"
        if remote:
            nonce = f"{time.time_ns()}"
            assert remote_bytes(manifest, nonce) == content, manifest
            assert remote_bytes(path, nonce) == image, path
            assert remote_bytes(path, nonce, "bytes=0-1023") == image[:1024], path
        print(f"PASS {manifest}: {fields['version']} {profile} {len(image)} bytes", flush=True)
    assert len(versions) == 1
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
