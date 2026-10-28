#!/usr/bin/env -S uv run
"""demo_practice_positions_instructor.py

Day 4, period 4 demo: practice positions. For each small position the pair writes
down a prediction of the number of legal moves, then lets Remus count them: the
start position, a king in check, and a pinned knight.
The student file demo_practice_positions.py leaves one # line for each line the pair types.
"""

from attacks import in_check
from board import EMPTY, parse_square, print_board, set_piece
from game_state import WHITE, new_game
from legal_moves import legal_moves
from moves import move_to_uci


def position(pieces: dict[str, str]) -> dict:
    """Build a state with White to move from {square name: piece}, such as {"e1": "K"}."""
    state = new_game()
    for row in range(8):
        for col in range(8):
            state["board"][row][col] = EMPTY
    for name, piece in pieces.items():
        set_piece(state["board"], parse_square(name), piece)
    return state


def compare(state: dict, prediction: int) -> None:
    """Print the board, the pair's prediction, and the number of legal moves Remus finds."""
    print_board(state["board"])
    count = len(legal_moves(state))
    print(f"You predicted {prediction}, Remus finds {count} legal moves")


def main():
    print("Part #1 - The Start Position")
    # Write your prediction first, then run the file
    prediction = 20
    compare(new_game(), prediction)

    print("Part #2 - A King in Check")
    # White: king on e1. Black: rook on e8 and king on a8. The rook checks down the e-file.
    state = position({"e1": "K", "e8": "r", "a8": "k"})
    print(f"White in check: {in_check(state, WHITE)}  (expected True)")
    prediction = 4
    compare(state, prediction)

    print("Part #3 - A Pinned Knight")
    # Put a White knight on e2, between the king and the rook
    state = position({"e1": "K", "e2": "N", "e8": "r", "a8": "k"})
    prediction = 4
    compare(state, prediction)
    # Count only the moves that start on e2
    knight_count = 0
    for move in legal_moves(state):
        if move_to_uci(move).startswith("e2"):
            knight_count += 1
    print(f"Legal knight moves: {knight_count}  (expected 0: the knight is pinned)")

    print("Part #4 - Your Own Position")
    # Change the pieces in Part #3, predict again, and run. Can a pinned rook move?


if __name__ == "__main__":
    main()
