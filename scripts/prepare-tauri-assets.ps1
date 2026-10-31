$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root "tauri-dist"

if (Test-Path -LiteralPath $dist) {
  Remove-Item -LiteralPath $dist -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$htmlSource = Join-Path $root "YellowSphere.html"
$htmlOut = Join-Path $dist "index.html"
Copy-Item -LiteralPath $htmlSource -Destination $htmlOut -Force

foreach ($assetName in @("favicon.png", "settings-icon.png")) {
  $assetSource = Join-Path $root "src\yellowsphere\assets\$assetName"
  if (-not (Test-Path -LiteralPath $assetSource)) {
    throw "Could not find required Tauri asset: $assetSource"
  }
  Copy-Item -LiteralPath $assetSource -Destination (Join-Path $dist $assetName) -Force
}

$html = [IO.File]::ReadAllText($htmlOut, [Text.Encoding]::UTF8)
$html = $html.Replace("src/yellowsphere/assets/favicon.png", "favicon.png")
$html = $html.Replace("src/yellowsphere/assets/settings-icon.png", "settings-icon.png")
$old = @'
        } catch (err) {
          const message = err && err.message ? err.message : String(err);
          console.error('Tauri native export failed.', err);
          uiStatus(`Tauri export failed: ${message}`, 'invalid');
          return null;
        }
'@
$new = @'
        } catch (err) {
          const message = err && err.message ? err.message : String(err);
          if (message === 'Export cancelled.') {
            uiStatus('Export cancelled.', '');
            return null;
          }
          console.error('Tauri native export failed; trying WebView download fallback.', err);
          try {
            downloadBlobInBrowser(blob, filename);
            uiStatus(`Tauri native export failed; started WebView download fallback for ${filename}.`, 'valid');
            return null;
          } catch (fallbackErr) {
            const fallbackMessage = fallbackErr && fallbackErr.message ? fallbackErr.message : String(fallbackErr);
            uiStatus(`Tauri export failed: ${message}; fallback failed: ${fallbackMessage}`, 'invalid');
            return null;
          }
        }
'@
$old = $old.Replace("`r`n", "`n")
$new = $new.Replace("`r`n", "`n")
if (-not $html.Contains($old)) {
  throw "Could not apply Tauri export fallback patch to generated index.html"
}
$html = $html.Replace($old, $new)
$scriptMatches = [regex]::Matches($html, '<script(?:\s[^>]*)?>(.*?)</script>', [Text.RegularExpressions.RegexOptions]::Singleline)
if ($scriptMatches.Count -eq 0) {
  throw "Could not find inline scripts while refreshing the Tauri CSP"
}
$scriptHashes = foreach ($match in $scriptMatches) {
  $bytes = [Text.Encoding]::UTF8.GetBytes($match.Groups[1].Value)
  $digest = [Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
  "'sha256-$([Convert]::ToBase64String($digest))'"
}
$cspPattern = "script-src 'self'(?: 'sha256-[^']+')*; script-src-attr"
$cspReplacement = "script-src 'self' $($scriptHashes -join ' '); script-src-attr"
$updatedHtml = [regex]::Replace($html, $cspPattern, $cspReplacement, 1)
if ($updatedHtml -eq $html) {
  throw "Could not refresh inline script hashes in the Tauri CSP"
}
$html = $updatedHtml
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($htmlOut, $html, $utf8NoBom)

Write-Host "Prepared Tauri assets in $dist"
