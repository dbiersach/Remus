#!/usr/bin/env -S uv run
"""python_lists_instructor.py

Day 1, period 3, Python lab 2: lists, for and range, len(), and nested lists.
The chess drill builds an 8x8 board of dots, sets up the pieces, and counts the
pawns in a row, the same board that board.py holds on Day 1, period 4.
The student file python_lists.py leaves one # line for each line the pair types.
"""


def main():
    print("Part #1 - A List of Pieces")
    back_rank = ["r", "n", "b", "q", "k", "b", "n", "r"]
    print(f"Pieces on Black's back rank: {len(back_rank)}  (expected 8)")
    # Index 3 is the fourth square from the a-file: the d-file
    print(f"The piece on the d-file: {back_rank[3]}  (expected q)")

    print("Part #2 - Visit Every Square with for and range")
    # range(8) counts 0, 1, 2, ..., 7: one number for each file
    for col in range(8):
        print(back_rank[col], end=" ")
    print()
    print("  (expected r n b q k b n r)")

    print("Part #3 - A Board Is a List of Rows")
    # Each row is a fresh list of 8 dots, so changing one row leaves the others alone
    board = []
    for row in range(8):
        board.append(["."] * 8)
    # Row 0 is rank 8, so Black's pieces fill rows 0 and 1, and White's rows 6 and 7
    board[0] = back_rank
    board[1] = ["p"] * 8
    board[6] = ["P"] * 8
    board[7] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    for row in range(8):
        line = ""
        for col in range(8):
            line += board[row][col] + " "
        print(line)
    print("  (expected the starting position, Black at the top)")

    print("Part #4 - Count the Pawns in a Row")
    # Play 1. e4: the pawn leaves e2 (row 6, col 4) and lands on e4 (row 4, col 4)
    board[6][4] = "."
    board[4][4] = "P"
    pawns = 0
    for piece in board[6]:
        if piece == "P":
            pawns += 1
    print(f"White pawns left on rank 2: {pawns}  (expected 7)")
    print(f"board[4][4] holds {board[4][4]}  (expected P, the pawn on e4)")


if __name__ == "__main__":
    main()
