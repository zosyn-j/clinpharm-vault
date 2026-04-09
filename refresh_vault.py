from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [
    [sys.executable, str(ROOT / 'build_source_registry.py')],
    [sys.executable, str(ROOT / 'scan_disputes.py')],
    [sys.executable, str(ROOT / 'build_vault_site.py')],
]


def main():
    for cmd in STEPS:
        print(f"==> Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, cwd=ROOT)
    print("Vault refresh complete")


if __name__ == '__main__':
    main()
