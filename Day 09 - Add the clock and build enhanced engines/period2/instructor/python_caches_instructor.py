#!/usr/bin/env -S uv run
"""python_caches_instructor.py

Day 9, period 2, Python lab 12: a dict as a cache with tuple keys, math.dist(),
and random.seed(). The chess drill remembers
how many paths a lone knight has, a small perft, the idea behind the RED color
version's transposition table.
The student file python_caches.py leaves one # line for each line the student pair types.
"""

import math
import random
import time

# The eight jumps of a knight, as (row change, column change)
KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


def knight_perft(square: tuple[int, int], depth: int) -> int:
    """Count the paths a lone knight can take in depth moves from a square."""
    # Row 0 is rank 8 and column 0 is file a, so g1 is (7, 6)
    if depth == 0:
        return 1
    total = 0
    for row_step, col_step in KNIGHT_JUMPS:
        row = square[0] + row_step
        col = square[1] + col_step
        if 0 <= row < 8 and 0 <= col < 8:
            total += knight_perft((row, col), depth - 1)
    return total


def remembered_perft(cache: dict, square: tuple[int, int], depth: int) -> int:
    """Return knight_perft from a square, computing each (square, depth) only once."""
    # A tuple can be a dict key, so one key holds both the square and the depth
    key = (square, depth)
    if key not in cache:
        cache[key] = knight_perft(square, depth)
    return cache[key]


def main():
    print("Part #1 - A Dict Remembers Answers")
    cache = {}
    start = time.perf_counter()
    first = remembered_perft(cache, (7, 6), 8)
    first_time = time.perf_counter() - start
    start = time.perf_counter()
    second = remembered_perft(cache, (7, 6), 8)
    second_time = time.perf_counter() - start
    print(f"First call: {first:,} in {first_time:.3f} s  (expected 811,156)")
    print(
        f"Second call: {second:,} in {second_time:.6f} s  (expected 811,156, at once)"
    )

    print("Part #2 - math.dist() Measures a Straight Line")
    # d4 is (row 4, col 3) and g7 is (row 1, col 6): three squares across, three up
    distance = math.dist((4, 3), (1, 6))
    print(f"From d4 to g7: {distance:.3f} squares  (expected 4.243)")

    print("Part #3 - random.seed() Repeats the Same Random Numbers")
    random.seed(2016)
    first_roll = random.randint(1, 6)
    random.seed(2016)
    second_roll = random.randint(1, 6)
    print(
        f"Same roll after the same seed: {first_roll == second_roll}  (expected True)"
    )


if __name__ == "__main__":
    main()
