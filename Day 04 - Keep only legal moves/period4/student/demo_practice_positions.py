#!/usr/bin/env -S uv run
"""demo_practice_positions.py

Day 4, period 4 demo: practice positions. For each small position the pair writes
down a prediction of the number of legal moves, then lets Remus count them: the
start position, a king in check, and a pinned knight.
Replace each line that holds only # with one line of code, then run the file.
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
    #
    #

    print("Part #2 - A King in Check")
    # White: king on e1. Black: rook on e8 and king on a8. The rook checks down the e-file.
    #
    #
    #
    #

    print("Part #3 - A Pinned Knight")
    # Put a White knight on e2, between the king and the rook
    #
    #
    #
    # Count only the moves that start on e2
    #
    #
        #
            #
    #

    print("Part #4 - Your Own Position")
    # Change the pieces in Part #3, predict again, and run. Can a pinned rook move?


if __name__ == "__main__":
    main()
