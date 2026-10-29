#!/usr/bin/env -S uv run
"""python_modules.py

Day 4, period 1, Python lab 6: modules, import, and __name__.
The lab sits in the Day 4, period 1 folder next to the Remus code from Day 3. It
imports board.py and move_generation.py instead of copying their code, and shows
why a file's main() runs only when VS Code runs that file itself.
Replace each line that holds only # with one line of code, then run the file.
"""

# Each import line reads another file of this folder by its name, without the .py
#
#
#
#
from moves import move_to_uci


def main():
    print("Part #1 - Every File Has a __name__")
    # The file that VS Code runs is named "__main__"; an imported file keeps its name
    #
    #
    print("board.py printed no board when it was imported: its main() did not run")

    print("Part #2 - Use Functions from Another File")
    #
    #
    #
    names = ""
    #
        #
    print(f"Knight moves from g1: {names}  (expected g1f3 g1h3)")

    print("Part #3 - Run the Imported File on Its Own")
    print("Open board.py in VS Code and click Run Python File")
    print("  (expected the start board: there board.py is __main__, so main() runs)")


if __name__ == "__main__":
    main()
