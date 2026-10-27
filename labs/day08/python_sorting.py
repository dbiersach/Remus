#!/usr/bin/env -S uv run
"""python_sorting.py

Day 8, period 2, Python lab 11: insert() into a list in order, float("inf"), and
time.perf_counter(). The chess drill sorts captures by the value of the piece
they take, starts a search for the best value at minus infinity, and times a
perft run: three tools that alpha-beta and move ordering use.
Replace each line that holds only # with one line of code, then run the file.
"""

import time

from game_state import new_game
from perft import perft

PIECE_VALUES = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9}  # In pawns


def victim_value(piece: str) -> int:
    """Return the value of a captured piece, in pawns."""
    return PIECE_VALUES[piece]


def main():
    print("Part #1 - insert() Puts the Biggest Victim First")
    victims = ["p", "r", "q", "n"]
    # Step past every piece worth at least as much, then insert the new piece there
    #
    #
        #
        #
        #
            #
        #
    #

    print("Part #2 - Start the Best at Minus Infinity")
    # Every real value beats minus infinity, so the first victim always becomes best
    #
    best_piece = ""
    #
        #
            #
            #
    #

    print("Part #3 - Time a perft Run")
    #
    #
    #
    #
    #


if __name__ == "__main__":
    main()
