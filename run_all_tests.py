#!/usr/bin/env -S uv run
"""run_all_tests.py

Run the tests of every Day folder, one folder at a time, and the reference-tool
tests in tests/. Each Day folder is a complete copy of Remus with the same module
names (board.py, search.py, ...), so each folder gets its own pytest run.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main():
    folders = sorted(ROOT.glob("Day *")) + [ROOT / "tests"]
    failed = []
    for folder in folders:
        print(f"Testing {folder}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(folder)], check=False
        )
        if result.returncode != 0:
            failed.append(folder.name)
    print(
        f"Folders tested: {len(folders)}; failed: {', '.join(failed) or 'none'}"
        "  (expected none)"
    )


if __name__ == "__main__":
    main()
