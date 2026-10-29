#!/usr/bin/env -S uv run
"""python_modules_instructor.py

Day 4, period 1, Python lab 6: modules, import, and __name__.
The lab sits in the Day 4, period 1 folder next to the Remus code from Day 3. It
imports board.py and move_generation.py instead of copying their code, and shows
why a file's main() runs only when VS Code runs that file itself.
The student file python_modules.py leaves one # line for each line the pair types.
"""

# Each import line reads another file of this folder by its name, without the .py
import board
from board import new_board, parse_square
from game_state import WHITE
from move_generation import knight_moves
from moves import move_to_uci


def main():
    print("Part #1 - Every File Has a __name__")
    # The file that VS Code runs is named "__main__"; an imported file keeps its name
    print(f"This file's __name__: {__name__}  (expected __main__)")
    print(f"board.py's __name__: {board.__name__}  (expected board)")
    print("board.py printed no board when it was imported: its main() did not run")

    print("Part #2 - Use Functions from Another File")
    start = new_board()
    square = parse_square("g1")
    moves = knight_moves(start, square, WHITE)
    names = ""
    for move in moves:
        names += move_to_uci(move) + " "
    print(f"Knight moves from g1: {names}  (expected g1f3 g1h3)")

    print("Part #3 - Run the Imported File on Its Own")
    print("Open board.py in VS Code and click Run Python File")
    print("  (expected the start board: there board.py is __main__, so main() runs)")


if __name__ == "__main__":
    main()
