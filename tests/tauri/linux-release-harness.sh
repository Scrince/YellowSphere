#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

build_packages=0
validate_artifacts=0
skip_rust_tests=0
skip_prepare=0
inside_docker=0
require_rpm_signature=0

original_args=("$@")
while (($
  case "$1" in
    --build-packages) build_packages=1 ;;
    --validate-artifacts) validate_artifacts=1 ;;
    --skip-rust-tests) skip_rust_tests=1 ;;
    --skip-prepare) skip_prepare=1 ;;
    --inside-docker) inside_docker=1 ;;
    --require-rpm-signature) require_rpm_signature=1 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

if [[ "$(uname -s)" == "Darwin" && $inside_docker -eq 0 ]]; then
  command -v docker >/dev/null || { echo "Docker is required to run the Linux harness from macOS." >&2; exit 1; }
  python3 scripts/prepare_tauri_assets.py
  find src-tauri tauri-dist -name '._*' -type f -delete
  exec docker run --rm --platform linux/amd64 \
    -e TMPDIR=/linux-target \
    -e PATH=/root/.cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    -v yellowsphere-tauri-linux-target:/linux-target \
    -v "$root:/workspace" -w /workspace \
    yellowsphere-tauri-linux-builder:22.04 \
    bash tests/tauri/linux-release-harness.sh "${original_args[@]}" --inside-docker --skip-prepare
fi

[[ "$(uname -s)" == "Linux" ]] || { echo "The Linux release harness must run on Linux or through its macOS Docker path." >&2; exit 1; }
[[ "$(uname -m)" == "x86_64" ]] || { echo "The Linux release harness requires an x86_64 environment." >&2; exit 1; }

pass() { printf '[PASS] %s\n' "$1"; }
run() { printf '[RUN] %s\n' "$1"; shift; "$@"; }
assert_file() {
  local path="$1" minimum="${2:-1}"
  [[ -f "$path" ]] || { echo "Missing required file: $path" >&2; exit 1; }
  local size
  size="$(stat -c '%s' "$path")"
  ((size >= minimum)) || { echo "File is unexpectedly small: $path ($size bytes)" >&2; exit 1; }
}
verify_manifest_hash() {
  local relative="$1" expected actual
  expected="$(grep -F "  $relative" docs/SHA256SUMS | awk '{print $1}' | tail -1)"
  [[ -n "$expected" ]] || { echo "No SHA-256 manifest entry for $relative" >&2; exit 1; }
  actual="$(sha256sum "$relative" | awk '{print $1}')"
  [[ "$actual" == "$expected" ]] || { echo "SHA-256 mismatch for $relative" >&2; exit 1; }
  printf '[PASS] %s SHA256=%s\n' "$relative" "$actual"
}

assert_file package.json
assert_file src-tauri/Cargo.toml
assert_file src-tauri/tauri.conf.json
assert_file YellowSphere.html 500000

version="$(python3 - <<'PY'
import json, re
from pathlib import Path
package = json.loads(Path('package.json').read_text())
config = json.loads(Path('src-tauri/tauri.conf.json').read_text())
cargo = Path('src-tauri/Cargo.toml').read_text()
match = re.search(r'(?ms)^\[package\].*?^version\s*=\s*"([^"]+)"', cargo)
assert match, 'Could not read Cargo package version'
assert package['version'] == config['version'] == match.group(1), 'Tauri versions are not synchronized'
assert config['identifier'] == 'com.yellowsphere.recovery', 'Unexpected Tauri identifier'
assert config['build']['frontendDist'] == '../tauri-dist', 'Unexpected frontendDist'
print(config['version'])
PY
)"
pass "Tauri identity/version configuration ($version)"

if ((skip_prepare == 0)); then run "Prepare Tauri frontend assets" python3 scripts/prepare_tauri_assets.py; fi
assert_file tauri-dist/index.html 500000
assert_file tauri-dist/favicon.png 1000
assert_file tauri-dist/settings-icon.png 1000
! grep -q 'src/yellowsphere/assets/' tauri-dist/index.html
grep -q 'Tauri native export failed; trying WebView download fallback.' tauri-dist/index.html
cmp -s tauri-dist/favicon.png src/yellowsphere/assets/favicon.png
cmp -s tauri-dist/settings-icon.png src/yellowsphere/assets/settings-icon.png
pass "Prepared frontend assets"

for icon in icon.ico icon.png icon.icns; do assert_file "src-tauri/icons/$icon" 1000; done
pass "Tauri bundle icons"

target_dir="${TMPDIR:-/tmp}/yellowsphere-tauri-linux-harness"
if ((skip_rust_tests == 0)); then
  command -v cargo >/dev/null || { echo "Cargo is required for Rust tests." >&2; exit 1; }
  run "Rust unit tests" env CARGO_TARGET_DIR="$target_dir" cargo test --manifest-path src-tauri/Cargo.toml
fi

validate_linux_set() {
  local raw="$1" deb="$2" rpm_file="$3"
  assert_file "$raw" 100000
  assert_file "$deb" 100000
  assert_file "$rpm_file" 100000
  file "$raw" | grep -q 'ELF 64-bit LSB pie executable, x86-64'
  [[ "$(dpkg-deb --field "$deb" Package)" == "yellow-sphere" ]]
  [[ "$(dpkg-deb --field "$deb" Version)" == "$version" ]]
  [[ "$(dpkg-deb --field "$deb" Architecture)" == "amd64" ]]
  [[ "$(rpm -qp --queryformat '%{NAME} %{VERSION} %{RELEASE} %{ARCH}' "$rpm_file")" == "yellow-sphere $version 1 x86_64" ]]
  rpm -qlp "$rpm_file" | grep -x '/usr/bin/yellowsphere' >/dev/null
  dpkg-deb --contents "$deb" | grep 'usr/bin/yellowsphere' >/dev/null
  if ((require_rpm_signature)); then rpm --checksig "$rpm_file" | grep -q 'digests signatures OK'; fi
  pass "Linux raw binary, Debian package, and RPM metadata"
}

if ((build_packages)); then
  command -v cargo >/dev/null || { echo "Cargo is required for Tauri builds." >&2; exit 1; }
  run "Build Linux Debian and RPM packages" env CARGO_TARGET_DIR="$target_dir" cargo tauri build --bundles deb,rpm --ci
  validate_linux_set \
    "$target_dir/release/yellowsphere" \
    "$target_dir/release/bundle/deb/YellowSphere_${version}_amd64.deb" \
    "$target_dir/release/bundle/rpm/YellowSphere-${version}-1.x86_64.rpm"
  mkdir -p releases/tauri/linux
  cp "$target_dir/release/yellowsphere" releases/tauri/linux/
  cp "$target_dir/release/bundle/deb/YellowSphere_${version}_amd64.deb" releases/tauri/linux/
  cp "$target_dir/release/bundle/rpm/YellowSphere-${version}-1.x86_64.rpm" releases/tauri/linux/
fi

if ((validate_artifacts)); then
  validate_linux_set \
    releases/tauri/linux/yellowsphere \
    "releases/tauri/linux/YellowSphere_${version}_amd64.deb" \
    "releases/tauri/linux/YellowSphere-${version}-1.x86_64.rpm"
  for relative in \
    releases/tauri/linux/yellowsphere \
    "releases/tauri/linux/YellowSphere_${version}_amd64.deb" \
    "releases/tauri/linux/YellowSphere-${version}-1.x86_64.rpm"; do
    verify_manifest_hash "$relative"
  done
  if find releases/tauri/linux -name '._*' -type f | grep -q .; then
    echo "AppleDouble files found in Linux release outputs." >&2
    exit 1
  fi
fi

pass "Tauri Linux release harness completed"
