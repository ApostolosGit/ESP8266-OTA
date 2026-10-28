"""Exercise the release checks without contacting GitHub or changing artifacts."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_release as release


class Response:
    def __init__(self, status, headers, body):
        self.status, self.headers, self.body = status, headers, body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return self.body


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.image = b"\xe9" + bytes(range(256)) * 32
        (self.root / "EnergyMeter_DDS238_SSD1309_Ver6_00_test.bin").write_bytes(self.image)
        self.fields = {
            "version": "6.00", "file": "EnergyMeter_DDS238_SSD1309_Ver6_00_test.bin",
            "size": str(len(self.image)), "md5": hashlib.md5(self.image).hexdigest(),
            "meter": "DDS238", "oled": "SSD1309", "core": "ESP8266-2.7.2",
            "credentials": "LittleFS-or-setup-portal", "transport": "https-range",
            "application": "energymeter", "platform_version": "1.00", "driver": "DDS238",
            "profile": "energymeter-dds238-ssd1309", "ota_protocol": "2", "build": "a" * 40,
            "source_sha256": "b" * 64, "sha256": hashlib.sha256(self.image).hexdigest(),
        }

    def manifest(self):
        return ("\n".join(f"{key}={value}" for key, value in self.fields.items()) + "\n").encode()

    def validate(self):
        with patch.object(release, "ROOT", self.root):
            return release.validate_manifest("manifest-dds.txt", self.manifest())

    def test_matching_profile_and_digests(self):
        fields, image = self.validate()
        self.assertEqual(fields, self.fields)
        self.assertEqual(image, self.image)

    def test_wrong_driver_display_profile_or_protocol_rejected(self):
        for key, value in (("driver", "JSY-MK333"), ("oled", "NONE"),
                           ("profile", "energymeter-dds238-none"), ("ota_protocol", "1"),
                           ("application", "platform"), ("build", "short"),
                           ("source_sha256", "invalid"), ("sha256", "0" * 64)):
            with self.subTest(key=key):
                previous = self.fields[key]
                self.fields[key] = value
                with self.assertRaises(AssertionError):
                    self.validate()
                self.fields[key] = previous

    def test_changed_binary_rejected(self):
        path = self.root / self.fields["file"]
        path.write_bytes(self.image[:-1] + b"x")
        with self.assertRaisesRegex(AssertionError, "MD5 mismatch"):
            self.validate()

    def test_duplicate_manifest_field_rejected(self):
        with self.assertRaises(AssertionError):
            release.parse_manifest(self.manifest() + b"profile=wrong\n")

    def test_http_range_requires_status_exact_span_and_complete_body(self):
        args = ("firmware.bin", "nonce", (4096, 8191), 10000)
        body = b"x" * 4096
        valid = Response(206, {"Content-Range": "bytes 4096-8191/10000"}, body)
        with patch.object(release.urllib.request, "urlopen", return_value=valid) as request:
            self.assertEqual(release.remote_bytes(*args), body)
            self.assertEqual(request.call_args.args[0].get_header("Range"), "bytes=4096-8191")
        for response in (Response(200, valid.headers, body),
                         Response(206, {"Content-Range": "bytes 0-4095/10000"}, body),
                         Response(206, valid.headers, body[:-1])):
            with patch.object(release.urllib.request, "urlopen", return_value=response):
                with self.assertRaises(AssertionError):
                    release.remote_bytes(*args)


class VentilationChecks(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.image = b"\xe9" + bytes(range(256)) * 64
        self.fields = {
            "version": "2.02", "file": "Ventilation_ESP8266_V2_02.bin",
            "size": str(len(self.image)), "md5": hashlib.md5(self.image).hexdigest(),
            "sha256": hashlib.sha256(self.image).hexdigest(),
            "meter": "VENTILATION", "application": "ventilation",
            "platform_version": "1.03", "driver": "DS18B20-DHT11", "oled": "NONE",
            "profile": release.VENTILATION_PROFILE, "ota_protocol": "2",
            "core": "ESP8266-2.7.2", "transport": "https-range",
            "credentials": "LittleFS-migration-or-setup-portal", "build": "c" * 40,
            "source_sha256": "d" * 64, "hardware_validation": "UNVERIFIED",
            "requires": "Ventilation-1.04+", "local_ip": "192.168.1.81",
        }
        (self.root / self.fields["file"]).write_bytes(self.image)

    def manifest(self):
        return ("\n".join(f"{key}={value}" for key, value in self.fields.items()) + "\n").encode()

    def validate(self):
        with patch.object(release, "ROOT", self.root):
            return release.validate_ventilation_manifest(self.manifest())

    def test_matching_ventilation_profile(self):
        fields, image = self.validate()
        self.assertEqual(fields, self.fields)
        self.assertEqual(image, self.image)

    def test_wrong_application_display_driver_and_metadata_rejected(self):
        for key, value in (("version", "1.08"), ("version", "2.00"), ("platform_version", "1.01"), ("meter", "DDS238"),
                           ("application", "energymeter"), ("driver", "DDS238"),
                           ("oled", "SSD1309"), ("profile", "ventilation-none"),
                           ("ota_protocol", "1"), ("local_ip", "192.168.1.80"),
                           ("source_sha256", "invalid"), ("build", "pending"),
                           ("hardware_validation", "VERIFIED")):
            with self.subTest(key=key):
                previous = self.fields[key]
                self.fields[key] = value
                with self.assertRaises(AssertionError):
                    self.validate()
                self.fields[key] = previous

    def test_legacy_filename_and_corrupt_bytes_rejected(self):
        previous = self.fields["file"]
        self.fields["file"] = "Ventilation_ESP8266_V2_02_source.bin"
        with self.assertRaisesRegex(AssertionError, "allowlist"):
            self.validate()
        self.fields["file"] = previous
        path = self.root / previous
        path.write_bytes(self.image[:-1])
        with self.assertRaisesRegex(AssertionError, "size"):
            self.validate()
        path.write_bytes(self.image[:-1] + b"x")
        with self.assertRaisesRegex(AssertionError, "MD5"):
            self.validate()

    def test_remote_check_covers_full_image_and_first_middle_final_ranges(self):
        content = self.manifest()
        observed = []

        def download(path, nonce, byte_range=None, total_size=None):
            observed.append((path, byte_range, total_size))
            if path == "manifest-ventilation.txt":
                return content
            if byte_range is None:
                return self.image
            start, end = byte_range
            return self.image[start:end + 1]

        with patch.object(release, "remote_bytes", side_effect=download):
            release.verify_remote_image("manifest-ventilation.txt", content, self.fields, self.image)
        spans = [item[1] for item in observed if item[1] is not None]
        length = len(self.image)
        self.assertEqual(spans, [(0, 4095), ((length - 4096) // 2, (length - 4096) // 2 + 4095),
                                 (length - 4096, length - 1)])


if __name__ == "__main__":
    unittest.main()
