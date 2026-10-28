#!/usr/bin/env -S uv run
"""play_battle.py

The Day 9 battle for this color version. Copy the visiting pair's color folder into
the Remus folder on this laptop, press Run in VS Code, and type the visitor's
color. Remus-BROWN plays two 10-minute games against it from the same opening,
White in game 1 and Black in game 2. The two games take about 20 minutes.
version_match.py, in the Remus folder above this one, plays the games and adds
them to games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path


def main():
    opponent = input("The visiting color, such as RED: ").strip().upper()
    match_path = Path(__file__).parent.parent / "version_match.py"
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run([sys.executable, str(match_path), "BROWN", opponent], check=True)


if __name__ == "__main__":
    main()
