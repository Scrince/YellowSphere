# YellowSphere

YellowSphere v1.6.7 is an offline seed recovery, deterministic key derivation, and encrypted seed-backup tool. The canonical standalone application is [`YellowSphere.html`](YellowSphere.html). It validates or generates BIP39 mnemonics, derives wallet addresses and private keys, imports or exports `.arc` seed backups, exports derived material, and generates address QR codes without contacting a server.

Use this tool only on a trusted offline machine. It handles seed phrases, BIP39 passphrases, private keys, extended private keys, WIF keys, Stellar secret seeds, Cardano private keys, and plaintext export files.

## Current Build

| Surface | Current role |
| --- | --- |
| `YellowSphere.html` | Promoted v1.6.6 production HTML and browser source of truth |
| `lts/YellowSphere_v1.6.4_LTS.html` | Archived v1.6.4 long-term-support browser build |
| `lts/YellowSphere_v1.6.2_LTS.html` | Archived v1.6.2 long-term-support browser build |
| `lts/YellowSphere_v1.6.0_LTS.html` | Archived v1.6.0 long-term-support browser build |
| `lts/YellowSphere_v1.5.0_LTS.html` | Archived v1.5.0 long-term-support browser build |
| `src/yellowsphere/assets/YellowSphere.html` | Packaged v1.6.6 HTML asset used by the Python GUI |
| `YellowSphere.py` | Compatibility launcher for Python GUI and CLI |
| Python CLI | Scripted derivation/export compatibility surface; coin coverage may differ from the browser GUI |
| PySide6 GUI | Desktop wrapper around the packaged HTML asset |
| Python distributions | v1.6.6 wheel and source archive are checked in under `releases/python/` |
| Tauri wrapper | v1.6.6 Windows, macOS, and Linux desktop artifacts are checked in under `releases/tauri/` |

Do not mix files from different releases. The root HTML, packaged assets, Python package, Tauri wrapper, documentation, and release artifacts should be treated as one build set.

## Safety Rules

1. Verify hashes before entering real seed material.
2. Disconnect Wi-Fi, Ethernet, Bluetooth, sync tools, and remote access.
3. Use a clean browser profile or live operating system when practical.
4. Do not paste seed phrases or private keys into online pages, chat systems, or hosted tools.
5. Export only what you need, store exports on encrypted media, then click **Clear All** and close the app.

No local recovery tool can protect secrets from malware, keyloggers, browser extensions, screen capture, clipboard monitors, firmware compromise, or an already-compromised operating system.

## Current HTML Features

- 12-word and 24-word BIP39 English mnemonic validation
- CSPRNG-based 12-word and 24-word mnemonic generation
- Numbered word grid and normalized textarea input
- Hidden-seed workflow for generated, imported, and successfully derived manually entered seeds
- Press-and-hold seed reveal
- BIP39 passphrase support with root fingerprint display
- Bitcoin, Bitcoin Cash, Litecoin, Dogecoin, Ethereum / ERC-20, BNB Chain, Avalanche C-Chain, Polygon, Cosmos / ATOM, Tron / TRC-20, Solana, Stellar, Cardano, and XRP derivation
- P2PKH, P2WPKH-P2SH, P2WPKH, and P2TR address output where supported
- Bitcoin Cash CashAddr output with legacy Base58 toggle
- Ethereum EIP-55 checksummed addresses
- Ethereum-compatible EIP-55 addresses for BNB Chain, Avalanche C-Chain, and Polygon
- Polygon PoS mainnet and Polygon Amoy testnet profiles
- XRP classic addresses, with QR destination-tag prompt
- SLIP-0010 Ed25519 derivation for Solana and Stellar
- Cardano Icarus/CIP-1852 Shelley base address derivation
- Encrypted and unprotected `.arc` seed import/export
- Password, keyfile, and keyfile + password `.arc` protection modes
- JSON, CSV, TXT, and PDF derived-output export
- Self-contained QR encoder and PNG export
- Light, Dark, Dark+, and Terminal themes
- Configurable 2/5/15-minute or Off session timeout (five-minute default),
  visible one-minute warning, and optional 15-second tab-switch grace period

## Quick Start

### Browser

Open the canonical file directly:

```text
YellowSphere.html
```

The browser app is local-file capable. Runtime recovery use does not require npm, Python, Tauri, a CDN, or internet access.

### Python GUI

```bash
python -m pip install -r requirements.txt
python YellowSphere.py --gui
```

The GUI uses PySide6 WebEngine to render the packaged HTML asset.

Build or install the v1.6.6 Python package from the current source tree:

```bash
python -m pip install .
yellowsphere --version
```

### Python CLI

```bash
python -m pip install .
python YellowSphere.py --help
```

Example:

```bash
python YellowSphere.py \
  --mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about" \
  --derivation "m/84'/0'/0'" \
  --script-type p2wpkh \
  --coin bitcoin \
  --count 5 \
  --output-format json
```

The Python CLI is a separate compatibility surface and may not match the active browser build. Run `python YellowSphere.py --help` for its current choices.

## Default HTML Paths

The v1.6.6 `YellowSphere.html` browser app uses the defaults below.

| Coin | Internal ID | Default path | Notes |
| --- | --- | --- | --- |
| Bitcoin | `bitcoin` | `m/0'` | YellowSphere-native default; UI initially selects P2WPKH |
| Bitcoin Cash | `bitcoincash` | `m/0'` | Default CashAddr, optional legacy Base58 |
| Litecoin | `litecoin` | `m/84'/2'/0'` | Native SegWit default |
| Dogecoin | `dogecoin` | `m/44'/3'/0'` | P2PKH default |
| Ethereum / ERC-20 | `ethereum` | `m/44'/60'/0'` | ERC-20 tokens use same account address |
| BNB Chain | `bnbchain` | `m/44'/60'/0'` | Ethereum-compatible secp256k1 account |
| Avalanche C-Chain | `avalanche` | `m/44'/60'/0'` | Ethereum-compatible C-Chain account |
| Polygon | `polygon` | `m/44'/60'/0'` | Polygon PoS mainnet; Amoy testnet available |
| Cosmos / ATOM | `cosmos` | `m/44'/118'/0'` | Cosmos Bech32 account address |
| Tron / TRC-20 | `tron` | `m/44'/195'/0'` | TRC-20 tokens use the same account address |
| Solana | `solana` | `m/44'/501'/0'` | SLIP-0010 Ed25519 |
| Stellar | `stellar` | `m/44'/148'/0'` | StrKey public and secret seed output |
| Cardano | `cardano` | `m/1852'/1815'/0'/0/0` | Shelley base address output |
| XRP | `xrp` | `m/44'/144'/0'` | Destination tags are not derived |

Auto script selection uses the first purpose component: `49'` -> P2WPKH-P2SH, `84'` -> P2WPKH, `86'` -> P2TR, otherwise P2PKH. Ethereum, BNB Chain, Avalanche C-Chain, Polygon, Tron, Cosmos, and XRP ignore UTXO script type and use account-address logic. Solana, Stellar, and Cardano use their coin-specific Ed25519-family derivation flows.

## `.arc` Seed Backups

Current v1.6.6 exports retain the historical YellowSphere ARC V2 outer armor text marker:

```text
YELLOWSPHERE-ARC-V2
<base64 compact JSON bundle>
```

Protected internal YellowSphere ARC V3 properties:

- 32-byte random salt
- 12-byte random nonce
- AES-256-GCM with a 128-bit authentication tag
- fixed 512-byte zero-padded plaintext and 528-byte ciphertext/tag output
- authenticated JSON metadata, including `credential_mode`, as GCM AAD
- SHA-512 password pre-hash followed by PBKDF2-HMAC-SHA512 with 1,000,000 iterations in Password mode
- HKDF-SHA512 in Keyfile and Keyfile + Password modes

Protection modes:

- Password: password string after Unicode NFKD normalization
- Keyfile: 64 random keyfile bytes encoded into an `arc-keyfile-v1:` secret
- Keyfile + Password: keyfile bytes and NFKD password mixed by HKDF-SHA512 into an `arc-combined-v1:` secret
- Unprotected: plaintext mnemonic JSON inside `.arc` armor, for controlled test/offline handling only

The `.arc` file stores the mnemonic only. It does not store the BIP39 passphrase.

### v1.6.6 Encryption Format

`YellowSphere.html` writes protected bundles with internal format
`yellowsphere-encrypted-seed-v3` while retaining the existing `YELLOWSPHERE-ARC-V2`
outer armor for parser compatibility. The decoded JSON `format` and `version`,
not the armor line, identify the cryptographic format.

YellowSphere ARC V3 changes include:

- AES-256-GCM with a 32-byte random salt, 12-byte random nonce, and 128-bit tag
- a 512-byte zero-padded plaintext payload so ciphertext size does not reveal
  whether the mnemonic contains 12 or 24 words
- authenticated bundle metadata, including `credential_mode`, supplied as
  AES-GCM additional authenticated data rather than a separate MAC field
- SHA-512 password pre-hashing followed by PBKDF2-HMAC-SHA512 at 1,000,000
  iterations for Password mode
- HKDF-SHA512 for high-entropy Keyfile mode and for the Keyfile + Password
  combined-secret path
- best-effort clearing of temporary password, keyfile, salt, and plaintext byte
  arrays after cryptographic use

New password-protected keyfiles use version 2 of
`yellowsphere-keyfile-enc-v1`: AES-256-GCM, a 12-byte nonce, SHA-512
password pre-hashing, and PBKDF2-HMAC-SHA512 at 1,000,000 iterations. Keyfile
magic and format values are authenticated as GCM additional data.

Version 1.6.6 retains all legacy YellowSphere ARC V1/V2 and encrypted-keyfile v1 import paths.
Old files are decrypted with their original KDF, cipher, MAC, and combined-mode
secret construction; newly exported v1.6.6 files use the upgraded formats.

## Derived Exports

| Format | Filename | Contents |
| --- | --- | --- |
| JSON | `YellowSphere_Derived_Keys_Addresses.json` | Full structured object and nested key/address material |
| CSV | `YellowSphere_Derived_Keys_Addresses.csv` | Flattened address rows |
| TXT | `YellowSphere_Derived_Keys_Addresses.txt` | Human-readable deterministic text report |
| PDF | `YellowSphere_Key_Export_<Coin>.pdf` | jsPDF A4 landscape export with extended keys and address table |
| QR PNG | `qr_<sanitized_address>.png` | Address URI QR image only |

JSON, CSV, TXT, and PDF exports can contain private keys. Treat them as critical secrets.

## HTML Test Harness

The Playwright harness serves the browser source selected in
`tests/fixtures/yellowsphere-app.js` from a loopback-only HTTP server and runs with
one worker for deterministic cryptographic and UI tests. Production v1.6.6
validation should target `YellowSphere.html`.

```bash
npm install
npx playwright install chromium
npm run test:html
```

Available commands:

- `npm test` runs every Playwright test.
- `npm run test:html` runs the browser UI smoke and encryption suites.
- `npm run test:smoke` runs generation, derivation, settings, QR, and PDF flows.
- `npm run test:crypto` runs YellowSphere ARC V3, encrypted-keyfile v2, tamper rejection,
  independent Web Crypto conformance, and legacy compatibility tests.

When a managed Playwright browser is unavailable, set
`PLAYWRIGHT_EXECUTABLE_PATH` to an installed Chromium-family executable. The
harness fails on browser console errors and uncaught page errors.

### Python Harness

The Python harness uses the standard library only and supports the project
minimum of Python 3.10:

```bash
npm run test:python
# or: python tests/python/run_tests.py
```

It covers known BIP39 and Bitcoin BIP84 vectors, mnemonic generation, YellowSphere ARC V2
round trips and tamper rejection, JSON/CSV/TXT formatting, CLI execution,
version synchronization, and packaged offline GUI assets.

### Tauri Release Harnesses

Run host-platform Tauri preflight checks and Rust unit tests without building
new artifacts:

```bash
npm run test:tauri
```

`test:tauri` dispatches to the Windows, macOS, or Linux harness for the current
host. Build and validate fresh platform packages with:

```bash
npm run test:tauri:windows
npm run test:tauri:macos
npm run test:tauri:linux
```

Validate already-published artifacts without rebuilding:

```bash
npm run test:tauri:windows:validate
npm run test:tauri:macos:validate
npm run test:tauri:linux:validate
```

All harnesses validate synchronized package/Cargo/Tauri versions, application
identity, prepared frontend assets, icons, and Rust tests. Platform checks add
MSI/NSIS metadata and Authenticode status on Windows; app versions,
architectures, code signatures, DMG integrity, and optional notarization on
macOS; and ELF architecture, Debian/RPM metadata and payloads, optional RPM
signatures, and SHA-256 manifest entries on Linux. From macOS, the Linux harness
runs in the documented Ubuntu 22.04 amd64 Docker builder.

`npm run test:release` runs Python, HTML, and Tauri preflight suites. Installer
building remains opt-in because it requires the Windows Tauri toolchain and can
take substantially longer.

## Documentation

The text files in `docs/` specify v1.6.6 behavior and preserve explicitly
labeled historical compatibility material where required. `YellowSphere.html`
is the normative v1.6.6 browser source. Historical release notes and hashes
continue to identify archived builds.

- `docs/UserGuide.txt`
- `docs/FileFormat.txt`
- `docs/Encryption.txt`
- `docs/Derivation.txt`
- `docs/QR.txt`
- `docs/Passphrase.txt`
- `docs/Recovery.txt`
- `docs/OpSec.txt`
- `docs/TestVectors.txt`
- `docs/Release_v1.6.1.txt`
- `docs/Release_v1.6.2.txt`
- `docs/Release_v1.6.6.txt`

The generated manual is:

```text
docs/YellowSphere_Manual.pdf
```

Build it with:

```bash
python scripts/build_manual_pdf.py
```

If your system Python lacks ReportLab, use the bundled Codex runtime or install the dependency in an isolated environment.

## Python Build

The Python package requires Python 3.10 or newer. Build the wheel and source
archive in an isolated environment:

```bash
python -m venv .venv-build
. .venv-build/bin/activate
python -m pip install --upgrade build
python -m build
```

Expected v1.6.6 outputs:

```text
dist/yellowsphere-1.6.6-py3-none-any.whl
dist/yellowsphere-1.6.6.tar.gz
```

The v1.6.6 Python wheel and source archive are checked in under
`releases/python/` and hashed in `docs/SHA256SUMS`. The wheel contains the
offline v1.6.6 HTML, jsPDF, favicon, and settings icon assets. Install GUI
dependencies separately with `python -m pip install ".[gui]"` when building from
source.

## Tauri Build

Prepare assets:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare-tauri-assets.ps1
```

or:

```bash
python scripts/prepare_tauri_assets.py
```

Build:

```bash
npm run tauri -- build
```

The equivalent direct Windows release command is:

```powershell
cargo tauri build --bundles msi,nsis --ci
```

The Windows build produces the standalone executable plus MSI and NSIS
installers. The v1.6.6 Windows release set is checked in under
`releases/tauri/windows/` and hashed in `docs/SHA256SUMS`:

```text
releases/tauri/windows/yellowsphere.exe
releases/tauri/windows/YellowSphere_1.6.6_x64_en-US.msi
releases/tauri/windows/YellowSphere_1.6.6_x64-setup.exe
```

macOS release builds can also be produced per architecture:

```bash
cargo tauri build --target x86_64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target aarch64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target universal-apple-darwin --bundles app,dmg --ci
```

The v1.6.6 macOS DMG set and direct-test app bundles are checked in under
`releases/tauri/macos/` and hashed in `docs/SHA256SUMS`.

Linux amd64 release packages can be produced on a Linux build host, or from a
Linux amd64 Docker builder, with:

```bash
cargo tauri build --bundles deb,rpm --ci
```

The v1.6.6 Linux raw binary, Debian package, and RPM package are checked in
under `releases/tauri/linux/` and hashed in `docs/SHA256SUMS`.

The Tauri wrapper uses the Rust `save_export` command and the `window.yellowsphereTauriSaveExport` bridge for PDF, JSON, CSV, TXT, `.arc`, keyfile, and QR PNG saves.

## Hash Verification

Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File 'YellowSphere.html','lts/YellowSphere_v1.6.4_LTS.html','lts/YellowSphere_v1.6.2_LTS.html','lts/YellowSphere_v1.6.0_LTS.html','lts/YellowSphere_v1.5.0_LTS.html',YellowSphere.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

macOS/Linux:

```bash
find YellowSphere.html lts/YellowSphere_v1.6.4_LTS.html lts/YellowSphere_v1.6.2_LTS.html lts/YellowSphere_v1.6.0_LTS.html 'lts/YellowSphere_v1.5.0_LTS.html' YellowSphere.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

Publish hashes for release artifacts with the exact build they came from. This
repository currently contains v1.6.6 browser, Python, Windows, macOS, and Linux
artifacts hashed in `docs/SHA256SUMS`. Archived
v1.6.2/v1.6.1/v1.6.0/v1.5.0 artifacts are kept under `releases/` for reference.

## PGP Release Signatures

The v1.6.6 standalone HTML application, Windows artifacts, and Python release
artifacts include detached ASCII-armored PGP signatures (`*.asc`) next to the
files they sign. The release-signing public key is checked in as:

```text
docs/YellowSphere_Release_Signing_2026_pubkey.asc
```

Release signing key:

```text
YellowSphere Release Signing (2026) <release@yellowsphere.local>
Fingerprint: 6A88 D329 DCF6 1A44 EF69 101B 019E C328 3B45 1469
```

Verify the key fingerprint before trusting release signatures:

```bash
gpg --show-keys docs/YellowSphere_Release_Signing_2026_pubkey.asc
```

Import the public key and verify an artifact:

```bash
gpg --import docs/YellowSphere_Release_Signing_2026_pubkey.asc
gpg --verify YellowSphere.html.asc YellowSphere.html
gpg --verify releases/tauri/windows/YellowSphere_1.6.6_x64-setup.exe.asc releases/tauri/windows/YellowSphere_1.6.6_x64-setup.exe
```

The checksum manifest is also signed:

```bash
gpg --verify docs/SHA256SUMS.asc docs/SHA256SUMS
```

## Repository Map

Use `git status` and `rg --files` to inspect the current workspace tree.

## License

Project-specific source and documentation are MIT licensed. Vendored third-party components retain their own upstream notices and license terms. See [LICENSE.md](LICENSE.md).
