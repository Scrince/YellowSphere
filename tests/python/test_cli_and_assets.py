from __future__ import annotations

import contextlib
import base64
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from yellowsphere import APP_VERSION
from yellowsphere.cli import main
from yellowsphere.gui import find_html_app, find_vendored_jspdf


ROOT = Path(__file__).resolve().parents[2]
MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


class CliTests(unittest.TestCase):
    def test_cli_json_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            main([
                "--mnemonic", MNEMONIC,
                "--derivation", "m/84h/0h/0h",
                "--script-type", "p2wpkh",
                "--coin", "bitcoin",
                "--count", "1",
                "--output-format", "json",
            ])
        output = json.loads(stdout.getvalue())
        self.assertEqual(output["accounts"][0]["receiving"][0]["address"], "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu")

    def test_compatibility_launcher_version(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "YellowSphere.py"), "--version"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.stdout.strip(), f"YellowSphere {APP_VERSION}")


class PackagingTests(unittest.TestCase):
    def test_python_and_project_versions_match(self) -> None:
        project_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', project_text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), APP_VERSION)

    def test_gui_finds_offline_html_and_vendored_jspdf(self) -> None:
        self.assertEqual(find_html_app().resolve(), (ROOT / "YellowSphere.html").resolve())
        jspdf = find_vendored_jspdf()
        self.assertIsNotNone(jspdf)
        self.assertGreater(jspdf.stat().st_size, 100_000)

    def test_packaged_html_asset_exists(self) -> None:
        packaged = ROOT / "src" / "yellowsphere" / "assets" / "YellowSphere.html"
        self.assertTrue(packaged.is_file())
        self.assertGreater(packaged.stat().st_size, 500_000)

    def test_inline_script_hashes_match_content_security_policy(self) -> None:
        html_paths = [
            ROOT / "YellowSphere.html",
            ROOT / "src" / "yellowsphere" / "assets" / "YellowSphere.html",
        ]
        for html_path in html_paths:
            with self.subTest(html=html_path):
                html = html_path.read_text(encoding="utf-8")
                allowed_hashes = set(re.findall(r"'(sha256-[^']+)'", html))
                inline_scripts = re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", html, re.IGNORECASE)
                actual_hashes = {
                    "sha256-" + base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
                    for script in inline_scripts
                }
                self.assertEqual(actual_hashes, allowed_hashes)


if __name__ == "__main__":
    unittest.main()
