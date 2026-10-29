#!/usr/bin/env -S uv run
"""python_dicts_instructor.py

Day 2, period 2, Python lab 4: dicts, dataclasses, aliasing, and copying.
The chess drill stores a game state in a dict, shows two names sharing one board,
fixes that with a copy, and describes a move with a dataclass, the way
game_state.py and moves.py do on Day 2, period 3.
The student file python_dicts.py leaves one # line for each line the student pair types.
"""

from copy import deepcopy
from dataclasses import dataclass

CASTLING_AT_START = "KQkq"  # All four castling moves are still allowed


# A dataclass is a record with named fields, written once and used for every move
@dataclass
class Move:
    from_square: str
    to_square: str


def main():
    print("Part #1 - A Dict Holds Named Facts")
    state = {"turn": "w", "castling": CASTLING_AT_START, "fullmove_number": 1}
    # Read a value by its key, inside [ ]
    print(f"Side to move: {state['turn']}  (expected w)")
    print(f"Castling rights: {state['castling']}  (expected KQkq)")
    # Store a new value under a key that is already there
    state["turn"] = "b"
    print(f"Side to move after White plays: {state['turn']}  (expected b)")

    print("Part #2 - Two Names for One Board")
    board = []
    for row in range(8):
        board.append(["."] * 8)
    # b2 = board gives the same board a second name: no new board is made
    b2 = board
    b2[4][4] = "P"
    print(f"board[4][4] is {board[4][4]}  (expected P, the change shows in both)")
    print(f"Same board? {b2 is board}  (expected True)")

    print("Part #3 - A Copy Is a New Board")
    # deepcopy copies the outer list and every row inside it
    b3 = deepcopy(board)
    b3[0][0] = "r"
    print(f"board[0][0] is {board[0][0]}  (expected ., the original stays the same)")
    print(f"b3[0][0] is {b3[0][0]}  (expected r)")
    print(f"Same board? {b3 is board}  (expected False)")
    print(f"Equal boards? {b3 == board}  (expected False, a8 differs)")

    print("Part #4 - A Dataclass Describes a Move")
    move = Move("e2", "e4")
    print(f"The pawn lands on {move.to_square}  (expected e4)")
    print(move)
    print("  (expected Move(from_square='e2', to_square='e4'))")


if __name__ == "__main__":
    main()
