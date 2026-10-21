#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

build_installers=0
validate_artifacts=0
skip_rust_tests=0
require_notarization=0

while (($
  case "$1" in
    --build-installers) build_installers=1 ;;
    --validate-artifacts) validate_artifacts=1 ;;
    --skip-rust-tests) skip_rust_tests=1 ;;
    --require-notarization) require_notarization=1 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

[[ "$(uname -s)" == "Darwin" ]] || { echo "The macOS release harness must run on macOS." >&2; exit 1; }

pass() { printf '[PASS] %s\n' "$1"; }
run() { printf '[RUN] %s\n' "$1"; shift; "$@"; }
assert_file() {
  local path="$1" minimum="${2:-1}"
  [[ -f "$path" ]] || { echo "Missing required file: $path" >&2; exit 1; }
  local size
  size="$(stat -f '%z' "$path")"
  ((size >= minimum)) || { echo "File is unexpectedly small: $path ($size bytes)" >&2; exit 1; }
}
verify_manifest_hash() {
  local relative="$1" expected actual
  expected="$(grep -F "  $relative" docs/SHA256SUMS | awk '{print $1}' | tail -1)"
  [[ -n "$expected" ]] || { echo "No SHA-256 manifest entry for $relative" >&2; exit 1; }
  actual="$(shasum -a 256 "$relative" | awk '{print $1}')"
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

run "Prepare Tauri frontend assets" python3 scripts/prepare_tauri_assets.py
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

target_dir="${TMPDIR:-/tmp}/yellowsphere-tauri-macos-harness"
if ((skip_rust_tests == 0)); then
  command -v cargo >/dev/null || { echo "Cargo is required for Rust tests." >&2; exit 1; }
  run "Rust unit tests" env CARGO_TARGET_DIR="$target_dir" cargo test --manifest-path src-tauri/Cargo.toml
fi

validate_app() {
  local app="$1" expected_arch="$2" found_version architectures
  assert_file "$app/Contents/Info.plist"
  assert_file "$app/Contents/MacOS/yellowsphere" 100000
  found_version="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$app/Contents/Info.plist")"
  [[ "$found_version" == "$version" ]] || { echo "Unexpected app version in $app: $found_version" >&2; exit 1; }
  architectures="$(lipo -archs "$app/Contents/MacOS/yellowsphere")"
  [[ "$architectures" == "$expected_arch" ]] || { echo "Unexpected architectures in $app: $architectures" >&2; exit 1; }
  codesign --verify --deep --strict --verbose=2 "$app"
  if ((require_notarization)); then
    xcrun stapler validate "$app"
  fi
  pass "$(basename "$app") version=$found_version architectures=$architectures"
}

validate_dmg() {
  local dmg="$1"
  assert_file "$dmg" 100000
  [[ "$(basename "$dmg")" == *"$version"* ]] || { echo "DMG filename does not contain $version: $dmg" >&2; exit 1; }
  hdiutil verify "$dmg" >/dev/null
  if ((require_notarization)); then
    xcrun stapler validate "$dmg"
  fi
  pass "$(basename "$dmg") passed hdiutil verification"
}

if ((build_installers)); then
  command -v cargo >/dev/null || { echo "Cargo is required for Tauri builds." >&2; exit 1; }
  for target in x86_64-apple-darwin aarch64-apple-darwin universal-apple-darwin; do
    run "Build $target app and DMG" env COPYFILE_DISABLE=1 APPLE_SIGNING_IDENTITY=- CARGO_TARGET_DIR="$target_dir" cargo tauri build --target "$target" --bundles app,dmg --ci
  done
  validate_app "$target_dir/x86_64-apple-darwin/release/bundle/macos/YellowSphere.app" "x86_64"
  validate_app "$target_dir/aarch64-apple-darwin/release/bundle/macos/YellowSphere.app" "arm64"
  validate_app "$target_dir/universal-apple-darwin/release/bundle/macos/YellowSphere.app" "x86_64 arm64"
  validate_dmg "$target_dir/x86_64-apple-darwin/release/bundle/dmg/YellowSphere_${version}_x64.dmg"
  validate_dmg "$target_dir/aarch64-apple-darwin/release/bundle/dmg/YellowSphere_${version}_aarch64.dmg"
  validate_dmg "$target_dir/universal-apple-darwin/release/bundle/dmg/YellowSphere_${version}_universal.dmg"
fi

if ((validate_artifacts)); then
  find releases/tauri/macos -name '._*' -type f -delete
  validate_app "releases/tauri/macos/YellowSphere x64.app" "x86_64"
  validate_app "releases/tauri/macos/YellowSphere.app" "arm64"
  validate_app "releases/tauri/macos/YellowSphere Universal.app" "x86_64 arm64"
  for suffix in x64 aarch64 universal; do
    relative="releases/tauri/macos/YellowSphere_${version}_${suffix}.dmg"
    validate_dmg "$relative"
    verify_manifest_hash "$relative"
  done
  
  find releases/tauri/macos -name '._*' -type f -delete
  if find releases/tauri/macos -name '._*' -type f | grep -q .; then
    echo "AppleDouble files found in macOS release outputs." >&2
    exit 1
  fi
fi

pass "Tauri macOS release harness completed"
