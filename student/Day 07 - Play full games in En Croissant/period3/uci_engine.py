#!/usr/bin/env -S uv run
"""uci_engine.py

Let a chess GUI such as En Croissant play against Remus. The GUI and Remus talk in
the Universal Chess Interface (UCI): the GUI sends one command per line, such as
"position startpos moves e2e4" or "go", and Remus answers "bestmove e7e5".

This first engine reads only games that begin from the starting position, and it
plays a random legal move. Day 7 teaches every UCI command, FEN positions, and
smarter brains.
"""

import random
import sys

from game_state import new_game
from legal_moves import legal_moves
from make_move import make_move
from moves import move_from_uci, move_to_uci

# The starting position as FEN text, the way En Croissant sends it
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def send(text: str) -> None:
    """Send one line to the GUI. flush=True makes it leave at once."""
    print(text, flush=True)


def set_position(words: list[str]) -> dict:
    """
    Build the state that a "position" command describes, such as
    "position startpos moves e2e4" or "position fen <the start FEN> moves e2e4".

    Parameters
    ----------
    words : list[str]
        The command split into words, such as
        ["position", "startpos", "moves", "e2e4", "e7e5"].

    Returns
    -------
    dict
        The game state after the listed moves.
    """
    state = new_game()
    # En Croissant sends the start position as FEN text, so both forms mean the start
    starts_at_start = words[1] == "startpos" or " ".join(words[2:8]) == START_FEN
    if not starts_at_start:
        print("Remus reads only the starting position until Day 7", file=sys.stderr)
    if "moves" in words:
        for text in words[words.index("moves") + 1 :]:
            make_move(state, move_from_uci(text, state["turn"] == "w"))
    return state


def main():
    state = new_game()
    for line in sys.stdin:
        words = line.split()
        if not words:
            continue
        command = words[0]
        if command == "uci":
            send("id name Remus")
            send("id author Turning a Chess Engine into Science AI")
            send("uciok")
        elif command == "isready":
            send("readyok")
        elif command == "ucinewgame":
            state = new_game()
        elif command == "position":
            state = set_position(words)
        elif command == "go":
            moves = legal_moves(state)
            if moves:
                send(f"bestmove {move_to_uci(random.choice(moves))}")
            else:
                send("bestmove 0000")  # Checkmate or stalemate: no move to play
        elif command == "quit":
            break
        else:
            print(f"Remus ignores: {line.strip()}", file=sys.stderr)


if __name__ == "__main__":
    main()
