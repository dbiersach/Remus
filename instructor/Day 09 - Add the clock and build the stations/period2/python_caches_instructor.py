#!/usr/bin/env -S uv run
"""python_caches_instructor.py

Day 9, period 2, Python lab 12: a dict as a cache with tuple keys, math.dist(),
and random.seed(). The chess drill remembers
perft counts it has already computed, the idea behind the RED station's
transposition table.
The student file python_caches.py leaves one # line for each line the pair types.
"""

import math
import random
import time

from game_state import new_game
from perft import perft


def remembered_perft(cache: dict, name: str, depth: int) -> int:
    """Return perft from the start position, computing each (name, depth) only once."""
    # A tuple can be a dict key, so one key holds both the position name and the depth
    key = (name, depth)
    if key not in cache:
        cache[key] = perft(new_game(), depth)
    return cache[key]


def main():
    print("Part #1 - A Dict Remembers Answers")
    cache = {}
    start = time.perf_counter()
    first = remembered_perft(cache, "start", 3)
    first_time = time.perf_counter() - start
    start = time.perf_counter()
    second = remembered_perft(cache, "start", 3)
    second_time = time.perf_counter() - start
    print(f"First call: {first:,} in {first_time:.3f} s  (expected 8,902)")
    print(f"Second call: {second:,} in {second_time:.6f} s  (expected 8,902, at once)")

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
