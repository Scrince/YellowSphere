                      
                                                                        

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    system = platform.system()
    if system == "Windows":
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        if not powershell:
            raise RuntimeError("PowerShell is required for the Windows release harness.")
        command = [
            powershell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "tests" / "tauri" / "windows-release-harness.ps1"),
        ]
    elif system == "Darwin":
        command = ["bash", str(ROOT / "tests" / "tauri" / "macos-release-harness.sh")]
    elif system == "Linux":
        command = ["bash", str(ROOT / "tests" / "tauri" / "linux-release-harness.sh")]
    else:
        raise RuntimeError(f"Unsupported release-harness platform: {system}")
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
