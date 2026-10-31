# Changelog - YellowSphere

All notable user-facing and compatibility-relevant changes are documented here.
The v1.6.7 source of truth is `YellowSphere.html` plus the byte-level
references in `docs/`. The previous v1.6.4 standalone build is archived under
`lts/`.

The project originally used a rolling `YellowSphere` release tag, then
`-production` suffixes, and now uses plain semantic versions for promoted
releases. Older entries below preserve that history while normalizing the
format.

## [Unreleased]

## [1.6.7-rc.2] - 2026-10-31

- Normalized the PowerShell preparation script's replacement snippets and made
  the Python preparation script strip the source HTML BOM so both generate
  byte-identical Tauri frontend assets.
- Fixed the Windows Tauri candidate build failure found in rc.1.

## [1.6.7-rc.1] - 2026-10-31

- Repaired the Playwright fixture server URL and the Linux/macOS release harness argument loops (issue #49).
- Prepared the offline browser, Python, and Tauri source set as version 1.6.7-rc.1.


## [1.6.6] - 2026-06-26

### Added

- Promoted the beta standalone HTML to the canonical `YellowSphere.html`
  filename and archived the previous production build as
  `lts/YellowSphere_v1.6.4_LTS.html`.
- Added Playwright coverage for keyfile file-picker import, keyfile drag-and-drop
  import, encrypted keyfile import, wrong-password handling, and CSP hash
  enforcement. The interaction tests build temporary `.arc` and keyfile contents
  in memory, avoiding external fixtures or dependencies.
- Added drag-and-drop support to keyfile import rows. Dropped keyfiles use the
  same validation, password handling, status messages, and credential-mode
  behavior as keyfiles selected with the file picker.
- Made the keyfile drop area more apparent with a persistent dashed outline,
  drop icon, clearer helper text, and a drag-over highlight.

### Changed

- Promoted the browser build to `1.6.6`.
- Updated the Python package metadata for YellowSphere v1.6.6 and published the
  rebuilt wheel and source archive under `releases/python/`.
- Kept drag-and-drop limited to keyfile loading; encrypted seed imports continue
  to use the `Import Seed` file picker.
- Deferred browser object-URL revocation for 10 seconds after initiating a
  download, improving reliability in Safari, Firefox, and other browsers while
  leaving the Tauri native export path unchanged.
- Consolidated output-panel and QR-modal `Escape` handling into one global
  keydown dispatcher.
- `handleClearAll` now cancels and resets pending idle-warning state, dismisses
  any visible idle countdown banner, and prevents stale countdown warnings after
  manual clears, visibility-security clears, or idle-timeout clears.

### Added

- Added a reusable Playwright test harness for `YellowSphere.html` with a
  worker-scoped local HTTP server, application-page fixture, browser console and
  page-error enforcement, and shared independent Web Crypto reference helpers.
- Added browser conformance tests for YellowSphere ARC V3 Password, Keyfile, and Keyfile +
  Password modes; fixed padding and field sizes; authenticated metadata and
  ciphertext tampering; wrong credentials; encrypted-keyfile v2; and legacy
  YellowSphere ARC V2/encrypted-keyfile v1 compatibility.
- Added `test`, `test:crypto`, and `test:html` npm commands alongside the focused
  `test:smoke` command.
- Added an optional `PLAYWRIGHT_EXECUTABLE_PATH` override for environments that
  provide a system Chromium-family browser instead of Playwright-managed
  Chromium.
- Added a dependency-free Python `unittest` harness covering BIP39 vectors,
  mnemonic generation, BIP84 derivation, YellowSphere ARC V2 encryption/armor/tamper
  rejection, CLI JSON output, launcher versioning, and packaged GUI assets.
- Added a Windows Tauri release harness that validates synchronized release
  identity, prepared frontend assets, bundle icons, Rust unit tests, and,
  optionally, MSI/NSIS builds, artifact sizes, hashes, versioned filenames, and
  Authenticode signatures.
- Added `test:python`, `test:tauri`, `test:tauri:windows`, and `test:release` npm
  commands for focused and combined release validation.

- Added protected `.arc` format v3 to `YellowSphere.html`. V3 uses
  AES-256-GCM, a 32-byte random salt, a 12-byte nonce, a 128-bit tag, and a
  fixed 512-byte padded plaintext payload.
- Added AES-256-GCM encrypted keyfile version 2 with authenticated keyfile magic
  and format metadata. Existing encrypted keyfile version 1 import remains
  supported.
- Added an authenticated `credential_mode` field to YellowSphere ARC V3 bundles with
  `password`, `keyfile`, or `both` values.

- Added a Settings -> Advanced `Tab-Switch Grace Period` toggle. The default
  behavior now waits 15 seconds before clearing sensitive fields when the tab
  is hidden, and cancels the pending clear if the user returns in time. The
  setting can be disabled to restore immediate clearing and is persisted
  locally.
- Added a persistent Settings -> Advanced `Session Timeout` selector with
  2-minute, 5-minute, 15-minute, and Off options. Five minutes remains the
  default, and timeout changes take effect immediately.
- Added a restrictive Content Security Policy that denies network connections,
  permits only the exact hashed inline scripts, and blocks script attributes,
  objects, frames, workers, media, manifests, and form submissions.

### Changed

- Changed new v1.6.6 Password-mode YellowSphere ARC V3 key derivation to SHA-512 pre-hashing
  followed by PBKDF2-HMAC-SHA512 at 1,000,000 iterations.
- Changed new v1.6.6 Keyfile-mode YellowSphere ARC V3 derivation to HKDF-SHA512. Combined mode
  now mixes raw keyfile bytes and NFKD-normalized password bytes with
  HKDF-SHA512 using the YellowSphere ARC salt and the fixed info string
  `yellowsphere-arc-v3-combined-key`.
- Changed newly generated password-protected keyfiles to SHA-512 password
  pre-hashing, PBKDF2-HMAC-SHA512 at 1,000,000 iterations, and AES-256-GCM with
  a 12-byte nonce. Existing 200,000-iteration version 2 keyfiles remain readable.
- YellowSphere ARC V3 authenticates all bundle metadata as AES-GCM additional authenticated
  data and no longer emits the YellowSphere ARC V2 separate MAC field.

- Debounced live root-fingerprint refreshes and serialized fingerprint and
  address-derivation work through latest-request-wins queues. Manual and
  automatic derivations can no longer overlap, queued stale work is collapsed,
  derivations take priority over fingerprint refreshes, and Clear All
  invalidates pending or in-flight results.
- Moved derivation-info icon event registration out of the seed-import path so
  its input and currency-change listeners are registered exactly once during
  UI initialization instead of accumulating after repeated imports.
- Embedded the favicon as a byte-identical base64 data URI so the standalone
  HTML no longer depends on a relative favicon path.
- Replaced the settings, QR export, and credential-dialog text close glyphs
  with a shared, consistently sized SVG close icon while retaining their
  accessible labels.
- Replaced heavyweight mnemonic validation with checksum-only validation where
  seed and master-key derivation are not required.
- Changed live root-fingerprint refreshes to use a fingerprint-only derivation
  path instead of creating immutable hex strings for the complete BIP39 seed
  and master private key on every refresh.

### Security

- Added best-effort zeroing of temporary password, keyfile, salt, padded
  plaintext, and decrypted-plaintext byte arrays in the new YellowSphere ARC V3 and
  encrypted-keyfile v2 paths.
- Preserved the legacy combined-secret construction exclusively for YellowSphere ARC V2
  decryption so existing Password, Keyfile, and Keyfile + Password backups
  remain recoverable.

- Added best-effort zeroing for temporary `Uint8Array` buffers containing
  mnemonic/passphrase encodings, BIP39 seed bytes, serialized private keys,
  chain codes, HMAC results, checksums, and derivation intermediates.
- Added cleanup of discarded BIP32, Ed25519/SLIP-0010, Cardano, Taproot, WIF,
  extended-private-key, and Stellar StrKey working buffers after use.
- JavaScript strings and `BigInt` values remain subject to JavaScript runtime
  garbage collection and cannot be reliably overwritten in place.

### Fixed

- Made YellowSphere ARC V3 credential mode explicit so Password-mode strings beginning with
  reserved keyfile prefixes cannot be misclassified or locked to the wrong
  import workflow.
- Cleared credential-dialog password, confirmation, file-input, and keyfile
  secret state on completion, cancellation, timeout, and visibility clearing.
- Made the password meter penalize exact repeated patterns and label its output
  as a rough character-diversity score rather than an entropy guarantee.
- Synchronized the Playwright fixture title expectation with v1.6.6.

- Fixed stale smoke-test assumptions for the document title and ambiguous
  Generate/Export button locators, and hardened local test-server teardown so
  HTTP keep-alive connections cannot stall the runner.
- Changed the Rust export unit-test fixture to write under the OS temporary
  directory instead of the user's Downloads folder, allowing restricted CI and
  sandboxed Windows release validation without changing production exports.

- Fixed the mojibake ellipsis in the Bitcoin Cash CashAddr example shown in
  Advanced Settings.

### Verified

- Verified YellowSphere ARC V3 Password, Keyfile, and Keyfile + Password modes against
  independent Web Crypto PBKDF2, HKDF, and AES-GCM derivations.
- Verified YellowSphere ARC V3 fixed-size padding, salt and nonce lengths, wrong-credential
  rejection, and rejection of modified metadata or ciphertext.
- Verified encrypted-keyfile v2 independently and confirmed encrypted-keyfile
  v1 plus YellowSphere ARC V2 Password, Keyfile, and combined-mode compatibility.

- Verified both inline scripts parse successfully and match the SHA-256 hashes
  authorized by the Content Security Policy.
- Verified the embedded favicon decodes to the exact original 3,976-byte PNG
  and that no external favicon path remains.
- Verified the promoted HTML introduces no new whitespace errors.

## [1.6.2] - 2026-06-17

### Release Identity

- Promoted the tested `YellowSphere_Beta.html` changes into the production
  `YellowSphere.html` file and updated the visible/browser version to
  YellowSphere v1.6.2.
- Removed the temporary beta HTML and beta changelog after promotion.
- Updated the Python package and CLI version to v1.6.2 and synchronized the
  Python GUI's packaged WebView asset with the production HTML.
- Updated Tauri package, application, and Rust crate metadata to v1.6.2.
- Rebuilt the Windows x64 executable, MSI, and NSIS installer.
- Built v1.6.2 macOS Tauri artifacts for Intel, Apple Silicon, and universal
  distribution.
- Built v1.6.2 Linux amd64 Tauri artifacts as a raw ELF, Debian package, and
  RPM package.

### Added

- Added a live search field beside the Extended Keys tab after derivation.
- Added case-insensitive partial matching across derived row data, including
  addresses and private-key fields; the table updates on every keystroke and
  reports the visible/total row count.
- Kept the same live filter available when the output panel is expanded, with
  a clear no-results message when no derived row contains the entered text.

### Verified

- Verified partial address and private-key searches, search clearing,
  no-results behavior, and filtering while the output panel is expanded.
- Verified the promoted production HTML reports YellowSphere v1.6.2.
- Verified the Python CLI reports v1.6.2 and completes deterministic Bitcoin
  derivation successfully.
- Verified the v1.6.2 Windows Tauri executable launches, the MSI reports
  ProductVersion 1.6.2, and the executable, MSI, and NSIS artifacts are
  unsigned as documented.
- Verified the v1.6.2 macOS app bundles report version 1.6.2, contain the
  expected x86_64, arm64, or universal Mach-O slices, pass ad-hoc codesign
  verification, and are packaged in valid DMGs.
- Verified the v1.6.2 Linux raw binary is an x86-64 ELF, the Debian package
  reports Version 1.6.2 / Architecture amd64, and the RPM reports Version
  1.6.2 / Architecture x86_64 / Signature none.

## [1.6.1] - 2026-06-17

### Release Identity

- Promoted the former `YellowSphere_Beta.html` build to the production
  `YellowSphere.html` filename and updated its visible/browser version to
  YellowSphere v1.6.1.
- Archived v1.6.0 as `lts/YellowSphere_v1.6.0_LTS.html`; its application title
  now identifies it as YellowSphere v1.6.0 LTS.
- Renamed the previous v1.5.0 LTS build to
  `lts/YellowSphere_v1.5.0_LTS.html`.
- Updated the Python GUI package to v1.6.1 and synchronized its packaged HTML
  asset with the production `YellowSphere.html` build.

### Added

- Added Polygon PoS support using Ethereum-compatible secp256k1 accounts,
  EIP-55 addresses, the standard `m/44'/60'/0'` account path, and Polygon Amoy
  testnet metadata.
- Promoted the beta testnet profiles and additional account networks into the
  production browser build, including Tron, BNB Chain, Avalanche C-Chain, and
  Cosmos / ATOM.
- Added a Settings -> Advanced `Testnet` toggle with per-network profiles for
  every supported production currency.
- Added UTXO testnet defaults by script family: `m/44'/1'/0'` for P2PKH,
  `m/49'/1'/0'` for wrapped SegWit, `m/84'/1'/0'` for native SegWit, and
  `m/86'/1'/0'` for Taproot.
- Added Bitcoin Cash `bchtest:` CashAddr output, Litecoin `tltc1` and testnet
  key encoding, Dogecoin testnet address/WIF prefixes, and Cardano
  `addr_test` Shelley addresses.
- Added testnet metadata for Ethereum, Tron, BNB Chain, Avalanche C-Chain,
  Polygon, Cosmos, Solana, Stellar, Cardano, and XRP.
- Added BIP39 autocomplete suggestions to the numbered mnemonic-entry grid.
- Added the standalone HTML browser smoke-test workflow and
  `npm run test:smoke` command.
- Added `docs/ThirdPartyNotices.txt` as the consolidated location for
  third-party attribution and license text removed from inline HTML comments.

### Removed

- Removed Polkadot and Monero from the v1.6.1 browser selector, derivation
  routing, exports, and QR URI handling.

### Compatibility Notes

- YellowSphere ARC V2 seed-backup encryption and import behavior are unchanged from v1.6.0.
- The Python GUI now embeds the v1.6.1 production browser application. The
  Python CLI derivation engine remains a separate compatibility surface.
- Promoted Tauri package, application, and Rust crate metadata to v1.6.1 and
  rebuilt the Windows x64 executable, MSI, and NSIS installer from the v1.6.1
  production browser application. macOS and Linux artifacts remain v1.6.0.

### Changed

- Replaced the coin datalist with a standard select control, alphabetized with
  Bitcoin pinned as the default.
- Derivation now selects the active network profile from the Testnet setting
  while preserving the selected currency in output metadata.
- Changing Bitcoin or Litecoin script type while Testnet is enabled updates
  the default path to the corresponding testnet purpose path.
- Generalized the Testnet setting across supported currencies.
- Cached QR modal elements in the shared element map and added reliable Escape
  handling for the modal fallback path.
- Added confirmation before `Generate Random Seed` replaces existing seed
  material.
- Added immediate clearing of seed, passphrase, and derived output when the
  browser tab loses visibility.
- Clipboard-copy failures in derived tables and extended-key views now surface
  a visible status message.
- Relocated inline jsPDF third-party attribution and license comments from
  `YellowSphere_Beta.html` into `docs/ThirdPartyNotices.txt` without changing
  executable HTML behavior.
- Cleaned garbled non-license comments in `YellowSphere_Beta.html` while leaving
  functional code unchanged.

### Verified

- Verified inline JavaScript parsing, standalone page initialization, seed
  generation, BIP39 validation, settings, output views, QR generation, and PDF
  export during the beta-to-production promotion.
- Verified mainnet/testnet derivation behavior for the currencies retained in
  the v1.6.1 production selector.
- Verified the promoted production build reports YellowSphere v1.6.1 and the
  archived v1.6.0 build reports YellowSphere v1.6.0 LTS.
- Verified the v1.6.1 Windows Tauri executable launches, embeds the v1.6.1
  prepared HTML asset, and produces versioned MSI and NSIS packages.

## [1.6.0] - 2026-06-14

### Release Identity

- Promoted the repaired beta line to the canonical `YellowSphere.html`
  v1.6.0 release.
- Kept the previous canonical HTML build as an LTS copy (now named
  `lts/YellowSphere_v1.5.0_LTS.html`).
- Updated Python package metadata, Tauri package metadata, Tauri app metadata,
  packaged HTML assets, and manual generation metadata for v1.6.0.
- Rewrote the root documentation and `docs/` technical references around the
  current byte-level behavior.
- Rebuilt `docs/YellowSphere_Manual.pdf` from the updated text sources.
- Built v1.6.0 macOS Tauri release artifacts for Intel, Apple Silicon, and
  universal macOS distribution.
- Built v1.6.0 Linux Tauri release artifacts for amd64 distribution.

### Added

- Bitcoin Cash derivation in the canonical HTML app, including CashAddr output
  and optional legacy Base58 display.
- Solana derivation using SLIP-0010 Ed25519 hardened paths and Base58 public
  address output.
- Stellar derivation using SLIP-0010 Ed25519, StrKey public addresses, and
  Stellar secret seed output.
- Monero derivation using SLIP-0010 Ed25519-derived spend material, private
  spend/view keys, public spend/view keys, and standard mainnet address output.
- Cardano Icarus/CIP-1852 Shelley base address derivation.
- `.arc` Password, Keyfile, and Keyfile + Password protection modes.
- Raw keyfile format `yellowsphere-keyfile-v1`.
- Encrypted keyfile format `yellowsphere-keyfile-enc-v1`.
- Unprotected armored `.arc` export mode for controlled offline/test handling.
- Manual-entry seed auto-mask after successful derivation, using the same hidden
  seed workflow as generated and imported seeds.
- Shared press-and-hold reveal behavior for generated, imported, and manually
  entered hidden seeds.
- Tauri v2 desktop wrapper around the canonical HTML app.
- Tauri native save bridge for PDF, JSON, CSV, TXT, `.arc`, keyfile, and QR PNG
  exports.
- GitHub Actions workflow for native Tauri builds.
- PySide6 WebEngine GUI shell around the packaged HTML app.
- Python package layout under `src/yellowsphere/`, optional GUI dependency,
  and package entry point.
- Terminal theme.
- Cross-platform Tauri asset preparation scripts for Windows, macOS, and Linux
  build hosts.
- macOS Tauri `.app` bundles and DMGs for `x86_64-apple-darwin`,
  `aarch64-apple-darwin`, and `universal-apple-darwin`.
- Linux Tauri amd64 release binary plus Debian `.deb` and RPM `.rpm` packages.

### Changed

- Current protected `.arc` export uses armored `YELLOWSPHERE-ARC-V2` text with
  PBKDF2-HMAC-SHA512, 1,000,000 iterations, 32-byte salt, 24-byte nonce,
  HMAC-SHA512 stream encryption, and HMAC-SHA512 authentication.
- YellowSphere ARC V2 import rejects iteration counts below 600,000.
- The v1.6.0 docs distinguish the full canonical HTML feature set from the
  narrower Python CLI compatibility surface.
- Tauri asset preparation byte-copies the canonical HTML to preserve Unicode
  seed-mask text and inline assets.
- PDF export uses the inline jsPDF bundle rather than an eval-based or remote
  loader.
- Tauri export failures are surfaced as explicit UI errors.
- Release documentation now treats checked-in `releases/` files as local build
  artifacts that require per-release hash verification.
- v1.6.0 macOS release `.app` bundles are ad-hoc signed and DMGs are generated
  from the signed app bundles.

### Fixed

- XRP QR payload formatting now uses `?dt=` with a valid separator.
- Tagless XRP QR output now appends `?dt=00000` for scanner compatibility.
- XRP QR rendering uses a dedicated 320 px renderer and wider modal sizing.
- QR canvas CSS now scales on narrow viewports without overflow.
- QR capacity selection accounts for terminator bits and removes an incorrect
  version-10 short-circuit.
- Repaired damaged inline jsPDF and stripped JavaScript conditionals in the
  beta line so standalone HTML and rebuilt Tauri apps initialize correctly.
- Preserved bullet-mask and Unicode UI text in packaged Tauri assets.
- Fixed listener accumulation around imported seed path/coin refresh behavior.
- Removed misleading XRP Taproot network metadata.
- Removed Litecoin QR URI ambiguity around Bitcoin-style `3...` addresses.
- Updated stale documentation that still described older release behavior.

### Compatibility Notes

- The canonical v1.6.0 HTML app supports Bitcoin, Bitcoin Cash, Litecoin,
  Dogecoin, Ethereum / ERC-20, Solana, Stellar, Monero, Cardano, and XRP.
- The Python CLI remains a compatibility/scripted surface for Bitcoin,
  Litecoin, Dogecoin, Ethereum, and XRP.
- Current `.arc` exports are armored YellowSphere ARC V2. Legacy JSON V2, Python V1,
  browser AES-GCM V1, and older PBKDF2-SHA256/XOR-HMAC import paths remain
  supported where implemented.

## [1.5.2-beta] - 2026-06-13

This was the beta stabilization line that became v1.6.0 after repair and
documentation cleanup.

### Added

- `YellowSphere_Beta.html` as the validation target before promotion to the
  main HTML.
- Manual-entry seed masking after successful derivation.
- Dedicated XRP QR renderer with larger canvas and `xrp-mode` modal sizing.
- Responsive QR canvas sizing.
- PySide6 WebEngine shell replacing the older Tkinter-oriented GUI path.
- Packaged Python modules for core derivation logic, CLI handling, GUI launch,
  and HTML assets.
- Vendored and packaged jsPDF assets for offline PDF export.
- Tauri desktop build structure, native export command, capability entry, and
  injected `window.yellowsphereTauriSaveExport` bridge.
- Windows Tauri executable, MSI, and NSIS setup artifacts.
- macOS Tauri `.app` and DMG build outputs for Apple Silicon, Intel, and
  universal packaging.

### Changed

- Embedded jsPDF directly in the HTML so raw HTML PDF export can work offline.
- Replaced a Base64/eval jsPDF loader with a raw inline script compatible with
  Tauri/WebView restrictions.
- Moved technical documentation and screenshots from `Documentation/` to
  `docs/`.
- Split Python code into package modules while keeping the root launcher.
- Updated release documentation, hash verification, and installation guidance
  for Windows, macOS, Linux, and universal macOS packages.

### Fixed

- Malformed XRP destination-tag QR URI missing the `?` separator.
- Tagless XRP QR scanner failures.
- QR version-selection capacity bug.
- Tauri/WebView PDF initialization without eval.
- Tauri native export writing silently to Downloads instead of prompting for a
  save location.
- Tauri asset-preparation mojibake and Unicode corruption.
- Damaged inline jsPDF block and stripped JavaScript conditionals after asset
  preparation.

## [1.5.0] - 2026-06-05

### Added

- BIP21/URI scheme auto-detection for QR payloads.
- Forced black-on-white QR rendering for scanner reliability.
- Four-module QR quiet zone.
- PDF key export through jsPDF, saved as `YellowSphere_Key_Export_<coin>.pdf`.
- PDF title block with coin, app version, UTC timestamp, and root fingerprint.
- PDF Extended Keys section and address table.
- Extended Keys output tab.
- Per-cell copy controls for address and private-key columns.
- Address Count `maxlength="15"`.
- Range input for deriving explicit `START-END` address indexes.
- Collapsible Advanced settings section.
- Opt-in Auto-Derive on settings change with 600 ms debounce.
- Expand/minimize control for the output panel.
- QR modal Edit button.

### Changed

- PDF became the default selected export format.
- PDF export removed the network label and improved coin display capitalization.
- PDF private-key column now uses WIF for UTXO coins and hex for Ethereum/XRP.
- Table View promotes Branch, Path, Address, and private-key columns.
- Table View displays key and hex fields without truncation and suppresses
  fields already shown in the Extended Keys tab or page metadata.
- XRP QR flow prompts for a destination tag/memo before rendering.
- Export option formerly labeled "Dump" was renamed to "PDF".

### Fixed

- QR matrix structural modules were no longer accidentally masked as data.
- QR mask XOR preserves boolean data-cell type.
- QR format bits are written to the correct positions.
- QR penalty scoring normalizes mixed matrix cell types.
- Imported-seed derivation info listeners are registered once at startup.
- XRP network definition no longer advertises spurious Taproot versions.
- Litecoin QR URI detection no longer claims Bitcoin-style `3...` addresses.

## [1.4.0] - 2026-06-03

### Added

- Passphrase visibility toggle with accessible show/hide labels.
- Clipboard countdown after Copy Seed.
- Five-minute inactivity auto-clear with a one-minute warning banner.
- Derived output Table View and Raw JSON tabs.
- Copy-per-row address buttons.
- Derivation progress indicator with UI yielding during large derivations.

### Changed

- Passphrase input defaults to masked password mode.
- Output area border handling was adjusted for the tabbed output wrapper.

## [1.3.0] - 2026-06-02

### Added

- QR Export modal with self-contained QR generation on canvas.
- QR PNG save and address-copy controls.
- Enter-to-generate behavior in the QR address input.
- Dark+ theme.
- Three-way Light / Dark / Dark+ theme selector.
- Clear All button.
- Derivation path tooltip for the YellowSphere-native `m/0'` default.

### Changed

- Show Seed moved into the seed row near other seed-state controls.
- Copy Seed and Clear All buttons were restyled to use the default button style.
- Theme preference moved to `localStorage` key `yellowsphereTheme` with migration
  from the older `yellowsphereDarkMode` setting.

## [1.2.0] - 2026-06-02

### Added

- Laptop/small-screen responsive breakpoint at `max-width: 1280px`.
- More compact default Python GUI geometry and widget padding.

### Changed

- 12-word mode hides word-grid slots 13 through 24.
- Mnemonic textarea default height reduced to two lines.
- Output textarea default height reduced to ten lines.
- Hidden seed mask changed from asterisks to bullet groups.
- HTML body min-height changed from `100vh` to `100dvh` for modern browser
  viewport behavior.

## [1.1.0] - 2026-06-01

### Added

- Generate Random Seed button for 12-word and 24-word BIP39 mnemonics.
- Browser mnemonic generation through `crypto.getRandomValues`.
- Python GUI mnemonic generation through `os.urandom`.
- Numbered word-entry grid replacing the original single-textarea-first input
  workflow.
- 12/24-word selector and paste distribution across word fields.
- CLI `--all-common` flag for common BIP44/BIP49/BIP84/BIP86 paths.
- CLI `--coin bitcoin|litecoin|dogecoin|ethereum|xrp`.
- CLI `--testnet` for Bitcoin testnet parameters.
- Version string surfaced in the UI and CLI.

### Changed

- Generated seeds use the hidden-seed workflow introduced for imported `.arc`
  files.
- Documentation and security guidance were updated for generation and word-grid
  entry.

## [YellowSphere] - 2026-04-24

First formal GitHub release, tagged at commit `e7cc84e`.

### Added

- Ethereum / ERC-20 address derivation.
- Offline Keccak-256 and EIP-55 checksum address support.
- ERC-20 export fields noting that Ethereum tokens use the same account
  address.
- XRP classic address derivation.
- Validation output for word count, wordlist validity, entropy bits, checksum
  bits, checksum match, BIP39 compliance, root fingerprint, keystore type,
  seed format, and passphrase warning.
- Deep validation output for BIP39 512-bit seed, master private key, and master
  chain code.
- Taproot/P2TR address derivation, Bech32m encoding, BIP86 purpose detection,
  taproot internal key fields, taproot tweak, taproot output key fields, and
  output key parity.
- HTML encrypted seed workflow with Encrypt/Export Seed, Import Seed, Show
  Seed press-and-hold, and inline root fingerprint display.
- Python GUI encrypted seed workflow matching the HTML flow.
- Shared `.arc` file format for HTML/Python compatibility.

### Changed

- Imported encrypted seeds remain hidden on screen while still usable for
  validation, derivation, and export.
- Common derivation handling was extended to include `m/86'/coin'/0'`.

### Compatibility

- Added import support for older encrypted seed formats while writing the shared
  `.arc` format for current exports.

## Pre-Release History

Earlier development included:

- Initial BIP39 validation for 12-word and 24-word English mnemonics.
- BIP32 secp256k1 derivation pipeline.
- Bitcoin, Litecoin, and Dogecoin support.
- P2PKH, P2WPKH-P2SH, and P2WPKH address derivation.
- BIP44, BIP49, and BIP84 derivation path table.
- JSON, CSV, and TXT export of derived keys and addresses.
- Python CLI mode with mnemonic, derivation, script type, count, and output
  format flags.
- Python desktop GUI launch through `--gui`.
- Original dark mode toggle.
- SHA-256 hash verification guidance.
- Initial security, contribution, license, and screenshot documentation.
