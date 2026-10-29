#!/usr/bin/env -S uv run
"""demo_promotion_instructor.py

Day 5, period 4 demo: promotion and underpromotion. White's pawn on b7 may become
a queen, a rook, a bishop, or a knight. Three of the four leave Black with no legal
move and no check, which is stalemate, a draw. Only the knight gives checkmate.
The student file demo_promotion.py leaves one # line for each line the student pair types.
"""

from attacks import in_check
from board import EMPTY, parse_square, print_board, set_piece
from game_state import BLACK, new_game
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from moves import Move


def puzzle_state() -> dict:
    """White: king c6, bishop b6, pawn b7. Black: king a6. White to move."""
    state = new_game()
    for row in range(8):
        for col in range(8):
            state["board"][row][col] = EMPTY
    set_piece(state["board"], parse_square("c6"), "K")
    set_piece(state["board"], parse_square("b6"), "B")
    set_piece(state["board"], parse_square("b7"), "P")
    set_piece(state["board"], parse_square("a6"), "k")
    state["castling"] = ""
    return state


def main():
    state = puzzle_state()
    print_board(state["board"])
    before = state_snapshot(state)

    print("Part #1 - Try All Four Promotions")
    # Predict first: which piece wins, and which ones only draw?
    for letter in "QRBN":
        move = Move(parse_square("b7"), parse_square("b8"), letter)
        undo = make_move(state, move)
        replies = len(legal_moves(state))
        # No legal reply is checkmate if Black is in check, and stalemate if not
        if replies > 0:
            result = f"{replies} legal replies"
        elif in_check(state, BLACK):
            result = "checkmate"
        else:
            result = "stalemate"
        print(f"  b8={letter}: {result}")
        undo_move(state, undo)
    print("  (expected stalemate for Q, R, and B, and checkmate for N)")

    print("Part #2 - Every Promotion Undoes Exactly")
    same = state_snapshot(state) == before
    print(f"Back at the puzzle position: {same}  (expected True)")


if __name__ == "__main__":
    main()
