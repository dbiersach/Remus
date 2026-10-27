#!/usr/bin/env -S uv run
"""python_caches.py

Day 9, period 2, Python lab 12: a dict as a cache with tuple keys, math.dist(),
random.seed(), and a teacher demo of threading.Event. The chess drill remembers
perft counts it has already computed, the idea behind the RED station's
transposition table.
Replace each line that holds only # with one line of code, then run the file.
"""
# pyright: reportReturnType=false
import math
import random
import threading
import time

from game_state import new_game
from perft import perft


def remembered_perft(cache: dict, name: str, depth: int) -> int:
    """Return perft from the start position, computing each (name, depth) only once."""
    # A tuple can be a dict key, so one key holds both the position name and the depth
    #
    #
        #
    #


def count_until_stopped(stop: threading.Event, counts: list[int]) -> None:
    """Add 1 to counts[0] again and again until another thread sets the stop flag."""
    while not stop.is_set():
        counts[0] += 1


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
    #
    #

    print("Part #3 - random.seed() Repeats the Same Random Numbers")
    #
    first_roll = random.randint(1, 6)
    random.seed(2016)
    second_roll = random.randint(1, 6)
    print(f"Same roll after the same seed: {first_roll == second_roll}  (expected True)")

    print("Part #4 - Teacher Demo: Stop a Thread with threading.Event")
    # think() runs in a thread like this one, and the UCI "stop" command sets the flag
    stop = threading.Event()
    counts = [0]
    worker = threading.Thread(target=count_until_stopped, args=(stop, counts))
    worker.start()
    time.sleep(0.2)
    stop.set()
    worker.join()
    print(f"The thread counted to {counts[0]:,} before the flag stopped it")


if __name__ == "__main__":
    main()
