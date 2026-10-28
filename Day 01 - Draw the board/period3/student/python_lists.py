#!/usr/bin/env -S uv run
"""python_lists.py

Day 1, period 3, Python lab 2: lists, for and range, len(), and nested lists.
The chess drill builds an 8x8 board of dots, sets up the pieces, and counts the
pawns in a row, the same board that board.py holds on Day 1, period 4.
Replace each line that holds only # with one line of code, then run the file.
"""


def main():
    print("Part #1 - A List of Pieces")
    back_rank = ["r", "n", "b", "q", "k", "b", "n", "r"]
    #
    # Index 3 is the fourth square from the a-file: the d-file
    #

    print("Part #2 - Visit Every Square with for and range")
    # range(8) counts 0, 1, 2, ..., 7: one number for each file
    #
        #
    #
    print("  (expected r n b q k b n r)")

    print("Part #3 - A Board Is a List of Rows")
    # Each row is a fresh list of 8 dots, so changing one row leaves the others alone
    #
    #
        #
    # Row 0 is rank 8, so Black's pieces fill rows 0 and 1, and White's rows 6 and 7
    #
    #
    #
    #
    #
        #
        #
            #
        #
    print("  (expected the starting position, Black at the top)")

    print("Part #4 - Count the Pawns in a Row")
    # Play 1. e4: the pawn leaves e2 (row 6, col 4) and lands on e4 (row 4, col 4)
    #
    #
    #
    #
        #
            #
    #
    #


if __name__ == "__main__":
    main()
