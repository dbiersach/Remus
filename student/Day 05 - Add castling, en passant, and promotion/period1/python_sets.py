#!/usr/bin/env -S uv run
"""python_sets.py

Day 5, period 1, Python lab 7: sets, membership with in, dict lookups, and
replace(). The chess drill keeps the castling rights as the string "KQkq" and
removes a letter when a king or rook leaves its home square, the job of
update_castling_rights() in make_move.py on Day 5, period 2.
Replace each line that holds only # with one line of code, then run the file.
"""


def main():
    print("Part #1 - A Set Holds Each Item Once")
    # The squares that pieces have moved away from, with no repeats
    #
    #
    #
    #
    #

    print("Part #2 - Ask a Question with in")
    #
    #

    print("Part #3 - Look Up a Right in a Dict")
    # Each home square guards castling rights: K is White's king side, q Black's queen side
    rights_lost = {"e1": "KQ", "h1": "K", "a1": "Q", "e8": "kq", "h8": "k", "a8": "q"}
    #
    #

    print("Part #4 - Remove Rights with replace()")
    rights = "KQkq"
    # replace("K", "") gives back a new string with every K taken out
    #
    #
    # Remove each letter a home square guards, one letter at a time
    #
        #
    #
    rights = rights.replace("k", "")
    print(f"Replacing a letter that is gone changes nothing: {rights}  (expected Q)")


if __name__ == "__main__":
    main()
