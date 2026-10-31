#!/usr/bin/env -S uv run
"""basic_test.py

The Day 9 basic test for this enhanced engine. Press Run in VS Code: Remus-GREEN plays
one 2-minute game against Remus-WHITE, which shows that the engine plays legal
moves to the end of a game. Nobody reads the result.
version_match.py, in the misc/designer folder, plays the games and adds
them to misc/games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path


def main():
    # The top Remus folder is the nearest folder above this one with pyproject.toml
    top = Path(__file__).parent
    for folder in Path(__file__).parents:
        if (folder / "pyproject.toml").exists():
            top = folder
            break
    match_path = top / "misc" / "designer" / "version_match.py"
    # The folder above this one holds this engine folder and its opponents
    engines = Path(__file__).parent.parent
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run(
        [
            sys.executable,
            str(match_path),
            "--engines",
            str(engines),
            "GREEN",
            "--games",
            "1",
            "--minutes",
            "2",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
