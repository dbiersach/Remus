#!/usr/bin/env -S uv run
"""console_game.py

Play chess in the terminal by typing moves in SAN, such as e4, Nf3, or O-O.
With "remus" as the first argument, Remus plays Black. Type "quit" to stop.
"""

import sys

from board import print_board
from fen import START_FEN, state_from_fen
from game_end import game_result
from make_move import make_move
from notation import move_to_san, parse_san
from search import negamax_move


def main():
    remus_plays_black = len(sys.argv) > 1 and sys.argv[1] == "remus"
    state = state_from_fen(START_FEN)
    while game_result(state) is None:
        print_board(state["board"])
        if remus_plays_black and state["turn"] == "b":
            move = negamax_move(state)
            print(f"Remus plays {move_to_san(state, move)}")
        else:
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
    print_board(state["board"])
    result, reason = game_result(state)
    print(f"Game over: {result} by {reason}")


if __name__ == "__main__":
    main()
