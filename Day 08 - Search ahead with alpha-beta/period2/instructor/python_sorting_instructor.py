#!/usr/bin/env -S uv run
"""python_sorting_instructor.py

Day 8, period 2, Python lab 11: insert() into a list in order, float("inf"), and
time.perf_counter(). The chess drill sorts captures by the value of the piece
they take, starts a search for the best value at minus infinity, and times a
perft run: three tools that alpha-beta and move ordering use.
The student file python_sorting.py leaves one # line for each line the student pair types.
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
    ordered = []
    for piece in victims:
        value = victim_value(piece)
        place = 0
        while place < len(ordered) and victim_value(ordered[place]) >= value:
            place += 1
        ordered.insert(place, piece)
    print(f"Victims, best first: {ordered}  (expected ['q', 'r', 'n', 'p'])")

    print("Part #2 - Start the Best at Minus Infinity")
    # Every real value beats minus infinity, so the first victim always becomes best
    best_value = -float("inf")
    best_piece = ""
    for piece in victims:
        if victim_value(piece) > best_value:
            best_value = victim_value(piece)
            best_piece = piece
    print(f"Best victim: {best_piece}, worth {best_value}  (expected q, worth 9)")

    print("Part #3 - Time a perft Run")
    start = time.perf_counter()
    count = perft(new_game(), 3)
    elapsed = time.perf_counter() - start
    print(f"perft(3) = {count:,}  (expected 8,902)")
    print(f"Total run time (sec): {elapsed:.3f}")


if __name__ == "__main__":
    main()
