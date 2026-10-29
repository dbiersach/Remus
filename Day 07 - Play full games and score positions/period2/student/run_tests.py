#!/usr/bin/env -S uv run
"""run_tests.py

Run every test in this folder. Open this file in VS Code and click the Run Python
File button (the triangle at the top right of the editor). pytest prints a dot for
each test that passes and an F for each test that fails, with a report below.
"""

import sys
from pathlib import Path

import pytest


def main():
    folder = Path(__file__).parent
    print(f"Testing {folder}")
    targets = [str(folder)]
    # No cache folder is left behind, and the exit code says if every test passed
    sys.exit(pytest.main([*targets, "-p", "no:cacheprovider"]))


if __name__ == "__main__":
    main()
