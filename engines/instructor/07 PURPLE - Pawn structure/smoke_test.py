#!/usr/bin/env -S uv run
"""smoke_test.py

The Day 9 smoke test for this enhanced engine. Press Run in VS Code: Remus-PURPLE plays
one 2-minute game against Remus-WHITE, which shows that the engine plays legal
moves to the end of a game. Nobody reads the result.
version_match.py, in the folder above this one, plays the games and adds
them to misc/games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path


def main():
    match_path = Path(__file__).parent.parent / "version_match.py"
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run(
        [sys.executable, str(match_path), "PURPLE", "--games", "1", "--minutes", "2"],
        check=True,
    )


if __name__ == "__main__":
    main()
