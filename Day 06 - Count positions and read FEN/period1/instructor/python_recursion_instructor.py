#!/usr/bin/env -S uv run
"""python_recursion_instructor.py

Day 6, period 1, Python lab 8: recursion, a function that calls itself.
The chess drill counts down, counts the leaves of a small tree of moves, and
counts the paths of a knight: three counts with the same shape as perft() in
perft.py on Day 6, period 2.
The student file python_recursion.py leaves one # line for each line the pair types.
"""

KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


def countdown(number: int) -> None:
    """Print number, number - 1, ..., 1, and then Go!"""
    # Base case: at 0 the function stops calling itself
    if number == 0:
        print("  Go!")
        return
    # Recursive case: print one number, then let a smaller call do the rest
    print(f"  {number}")
    countdown(number - 1)


def count_leaves(tree: list | str) -> int:
    """
    Count the leaves of a tree of moves.

    Parameters
    ----------
    tree : list | str
        A move name such as "e5" is a leaf. A list holds the branches under one move.

    Returns
    -------
    int
        The number of leaves in the whole tree.
    """
    if isinstance(tree, str):
        return 1
    total = 0
    for branch in tree:
        total += count_leaves(branch)
    return total


def knight_paths(row: int, col: int, jumps: int) -> int:
    """Count the ways a knight on (row, col) can make this many jumps on an empty board."""
    if jumps == 0:
        return 1
    count = 0
    for row_step, col_step in KNIGHT_JUMPS:
        new_row = row + row_step
        new_col = col + col_step
        if 0 <= new_row <= 7 and 0 <= new_col <= 7:
            count += knight_paths(new_row, new_col, jumps - 1)
    return count


def main():
    print("Part #1 - Count Down")
    countdown(3)
    print("  (expected 3, 2, 1, Go!)")

    print("Part #2 - Count the Leaves of a Tree")
    # White's first moves e4, d4, and Nf3, each with Black's replies under it
    tree = [["e5", "c5"], ["d5"], ["Nf6", "e6", "d6"]]
    print(f"Leaves: {count_leaves(tree)}  (expected 6)")
    print(f"Leaves under e4: {count_leaves(tree[0])}  (expected 2)")

    print("Part #3 - Count the Paths of a Knight")
    # A knight on a1 (row 7, col 0) has two jumps, to b3 and c2
    print(f"One jump from a1: {knight_paths(7, 0, 1)}  (expected 2)")
    # Predict before you run: from b3 a knight has 6 jumps and from c2 it has 6
    print(f"Two jumps from a1: {knight_paths(7, 0, 2)}  (expected 12)")
    print(f"Three jumps from a1: {knight_paths(7, 0, 3)}  (expected 64)")


if __name__ == "__main__":
    main()
