#!/usr/bin/env -S uv run
"""play_tournament.py

The Day 10 tournament for this station. Press Run in VS Code: Remus-ORANGE plays
two 10-minute games against Remus-WHITE from the same opening, White in game 1
and Black in game 2. The two games take about 20 minutes.
station_match.py, in the Remus folder above this one, plays the games and adds
them to games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path


def main():
    match_path = Path(__file__).parent.parent / "station_match.py"
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run([sys.executable, str(match_path), "ORANGE"], check=True)


if __name__ == "__main__":
    main()
