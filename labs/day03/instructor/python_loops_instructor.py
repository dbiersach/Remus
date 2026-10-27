#!/usr/bin/env -S uv run
"""python_loops_instructor.py

Day 3, period 1, Python lab 5: while, break, and direction tuples.
The chess drill walks from d4 toward the edge of the board, one square at a time,
and stops at the first piece in the way: the same walk a bishop, rook, or queen
makes in move_generation.py on Day 3, period 3.
The student file python_loops.py leaves one # line for each line the pair types.
"""

BOARD_FILES = "abcdefgh"  # File letters, indexed by column: column 0 is file a
BOARD_RANKS = "87654321"  # Rank digits, indexed by row: row 0 is rank 8


def square_name(row: int, col: int) -> str:
    """Return the name of a square, such as "d4" for row 4, col 3."""
    return BOARD_FILES[col] + BOARD_RANKS[row]


def main():
    print("Part #1 - Repeat with while")
    # A while loop repeats as long as its test is True
    count = 0
    while count < 3:
        print(f"  step {count}")
        count += 1
    print("  (expected step 0, step 1, step 2)")

    print("Part #2 - A Direction Is a Tuple")
    # Row 0 is rank 8, so a step toward rank 8 makes the row smaller: -1
    up_right = (-1, 1)
    row_step, col_step = up_right
    print(f"row step {row_step}, col step {col_step}  (expected -1 and 1)")

    print("Part #3 - Walk Until the Edge or a Piece")
    board = []
    for row in range(8):
        board.append(["."] * 8)
    board[1][6] = "p"  # A Black pawn on g7
    # Start on d4: row 4, col 3
    row, col = 4, 3
    squares = ""
    while True:
        row += row_step
        col += col_step
        # Leaving the board ends the walk
        if row < 0 or row > 7 or col < 0 or col > 7:
            break
        squares += square_name(row, col) + " "
        # A piece on the square ends the walk too, after the square is counted
        if board[row][col] != ".":
            break
    print(f"Squares reached: {squares}  (expected e5 f6 g7)")

    print("Part #4 - Try Another Direction")
    # Change up_right in Part #2 to (-1, -1), up and to the left, and run again
    print("  (with (-1, -1) the walk reaches c5 b6 a7 and stops at the edge)")


if __name__ == "__main__":
    main()
