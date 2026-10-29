#!/usr/bin/env -S uv run
"""python_input_output_instructor.py

Day 7, period 2, Python lab 10: random.choice(), a best-so-far loop, sys.stdin,
print(..., flush=True), and sys.stderr. The chess drill picks a random move, picks
the most valuable capture, and answers "isready" with "readyok", the way the
first brains and the UCI engine do in period 3.
The student file python_input_output.py leaves one # line for each line the student pair types.
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
    pick = random.choice(moves)
    print(f"Random move: {pick}  (expected one of the four)")

    print("Part #2 - A Loop Keeps the Best Item So Far")
    # Start with the first piece, then swap in any piece worth more
    victims = ["p", "q", "n"]
    best = victims[0]
    for piece in victims:
        if victim_value(piece) > victim_value(best):
            best = piece
    print(f"Most valuable capture: {best}  (expected q)")

    print("Part #3 - Notes Go to stderr")
    # A GUI reads stdout, so notes for people go to stderr where the GUI ignores them
    print("This note goes to stderr", file=sys.stderr)

    print("Part #4 - Read Commands from stdin and Answer")
    print("Type isready, then hello, then quit, pressing Enter after each")
    for line in sys.stdin:
        command = line.strip()
        if command == "quit":
            break
        # flush=True sends the answer right away instead of keeping it in a buffer
        if command == "isready":
            print("readyok", flush=True)
        else:
            print(f"echo {command}", flush=True)
    print("  (expected readyok, then echo hello)")


if __name__ == "__main__":
    main()
