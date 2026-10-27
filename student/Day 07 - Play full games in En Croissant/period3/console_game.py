#!/usr/bin/env -S uv run
"""console_game.py

Two players take turns typing moves in SAN, such as e4, Nf3, or O-O.
Type "quit" to stop.
"""

from board import print_board
from fen import START_FEN, state_from_fen
from game_end import game_result
from make_move import make_move
from notation import parse_san


def main():
    state = state_from_fen(START_FEN)
    while True:
        print_board(state["board"])
        outcome = game_result(state)
        if outcome is not None:
            break  # The game is over
        text = input(f"{'White' if state['turn'] == 'w' else 'Black'} to move: ")
        if text.strip() == "quit":
            print("Game stopped.")
            return
        try:
            move = parse_san(state, text)
        except ValueError as error:
            print(error)
            continue
        make_move(state, move)
    result, reason = outcome
    print(f"Game over: {result} by {reason}")


if __name__ == "__main__":
    main()
