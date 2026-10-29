#!/usr/bin/env -S uv run
"""play_battle.py

The Day 9 battle: Remus-ORANGE on this laptop plays the engine of a visiting student pair.

1. The visiting student pair brings its engine folder on a USB stick, such as
   09 BLUE - Killer moves, copied from period2 > student > engines on its own laptop.
2. On this laptop, open File Explorer and go to the Remus folder, then
   Day 09 - Add the clock and build enhanced engines > period2 > student > engines.
3. Drag the visitor's engine folder from the USB stick into that engines folder.
   When Windows asks, choose Replace the files in the destination. The folder it
   replaces holds only stubs, because no student pair on this laptop writes that engine.
4. In VS Code, open this file, play_battle.py, in the ORANGE engine folder.
5. Set VISITING_ENGINE below to the visitor's engine color, such as "BLUE", and save.
6. Press the Run Python File button. Remus-ORANGE plays two 10-minute games against
   the visitor from the same opening, with the White pieces in game 1 and the Black
   pieces in game 2. The two games take about 20 minutes.
version_match.py, in the engines folder above this one, plays the games and adds
them to misc/games/remus_games.pgn.
"""

import subprocess
import sys
from pathlib import Path

# The visitor's engine color, such as "BLUE" (step 5 above)
VISITING_ENGINE = ""


def main():
    if VISITING_ENGINE == "":
        print("Set VISITING_ENGINE at the top of this file, then press Run again.")
        return
    match_path = Path(__file__).parent.parent / "version_match.py"
    print(f"Running {match_path}")
    # sys.executable is the Python that VS Code runs, with python-chess
    subprocess.run(
        [sys.executable, str(match_path), "ORANGE", VISITING_ENGINE.upper()], check=True
    )


if __name__ == "__main__":
    main()
