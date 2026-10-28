#!/usr/bin/env -S uv run
"""run_all_tests.py

Run the tests of every period's instructor folder and every version folder, one
folder at a time, and the reference-tool tests in misc/scripts/. Each folder is a complete
copy of Remus with the same module names (board.py, search.py, ...), so each folder
gets its own pytest run.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/scripts/


def main():
    folders = []
    for folder in sorted(ROOT.glob("Day */period*/instructor")):
        if list(folder.glob("test_*.py")):
            folders.append(folder)  # Periods before any Remus code have no tests
    day_9 = next(ROOT.glob("Day 09 - *"))
    engines = day_9 / "period2" / "instructor" / "engines"
    folders += sorted(engines.glob("* - *"))
    folders.append(engines / "Remus-GOLD")
    folders.append(ROOT / "misc" / "scripts")  # test_reference_tools.py
    failed = []
    for folder in folders:
        print(f"Testing {folder}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(folder)], check=False
        )
        if result.returncode != 0:
            failed.append(str(folder.relative_to(ROOT)))
    print(
        f"Folders tested: {len(folders)}; failed: {', '.join(failed) or 'none'}"
        "  (expected none)"
    )


if __name__ == "__main__":
    main()
