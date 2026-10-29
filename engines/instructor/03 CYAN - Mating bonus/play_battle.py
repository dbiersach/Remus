#!/usr/bin/env -S uv run
"""play_battle.py

The Day 9 battle: Remus-CYAN on this laptop plays the engine of a visiting student pair.

1. The visiting student pair copies its finished engine folder, such as
   Remus > engines > student > 09 BLUE - Killer moves, onto its USB stick.
2. On this laptop, the visitors paste that folder into the same path,
   Remus > engines > student. When Windows asks, choose Replace the files in the
   destination: the folder there holds only stubs, because no student pair on this
   laptop writes that engine.
3. In VS Code, open this file, play_battle.py, in the CYAN engine folder.
4. Set VISITING_ENGINE below to the visitor's engine color, such as "BLUE", and save.
5. Press the Run Python File button. Remus-CYAN plays two 10-minute games against
   the visitor from the same opening, with the White pieces in game 1 and the Black
   pieces in game 2. The two games take about 20 minutes.
version_match.py, in the folder above this one, plays the games and adds
them to misc/games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path

# The visitor's engine color, such as "BLUE" (step 4 above)
VISITING_ENGINE = ""


def main():
    if VISITING_ENGINE == "":
        print("Set VISITING_ENGINE at the top of this file, then press Run again.")
        return
    match_path = Path(__file__).parent.parent / "version_match.py"
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run(
        [sys.executable, str(match_path), "CYAN", VISITING_ENGINE.upper()], check=True
    )


if __name__ == "__main__":
    main()
