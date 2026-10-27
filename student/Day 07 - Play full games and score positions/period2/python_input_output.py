#!/usr/bin/env -S uv run
"""python_input_output.py

Day 7, period 2, Python lab 10: random.choice(), max() with key=, sys.stdin,
print(..., flush=True), and sys.stderr. The chess drill picks a random move, picks
the most valuable capture, and answers "isready" with "readyok", the way the
first brains and the UCI engine do in period 3.
Replace each line that holds only # with one line of code, then run the file.
"""

import random
import sys

PIECE_VALUES = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9}  # In pawns


def victim_value(piece: str) -> int:
    """Return the value of a captured piece, in pawns."""
    return PIECE_VALUES[piece]


def main():
    print("Part #1 - random.choice() Picks One Item")
    random.seed(2016)  # The same seed gives the same pick on every run
    moves = ["e2e4", "d2d4", "g1f3", "c2c4"]
    #
    #

    print("Part #2 - max() with key= Picks the Best Item")
    # key=victim_value makes max() compare the pieces by their values
    victims = ["p", "q", "n"]
    #
    #

    print("Part #3 - Notes Go to stderr")
    # A GUI reads stdout, so notes for people go to stderr where the GUI ignores them
    #

    print("Part #4 - Read Commands from stdin and Answer")
    print("Type isready, then hello, then quit, pressing Enter after each")
    #
        #
        #
            #
        # flush=True sends the answer right away instead of keeping it in a buffer
        #
            #
        #
            #
    print("  (expected readyok, then echo hello)")


if __name__ == "__main__":
    main()
