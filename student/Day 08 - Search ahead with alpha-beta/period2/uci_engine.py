#!/usr/bin/env -S uv run
"""uci_engine.py

Talk to a chess GUI such as Lucas Chess through the Universal Chess Interface (UCI).
The GUI sends one command per line on standard input, and Remus answers on standard
output. Debug text goes to standard error, where the GUI ignores it.

The first argument picks the brain: "random", "greedy", or "negamax" (the default).
"""

import sys

from fen import START_FEN, state_from_fen
from legal_moves import legal_moves
from make_move import make_move
from moves import move_from_uci, move_to_uci
from search import greedy_move, negamax_move, random_move

BRAINS = {
    "random": random_move,
    "greedy": greedy_move,
    "negamax": negamax_move,
}  # By name


def send(text: str) -> None:
    """Send one line to the GUI. flush=True makes it leave at once."""
    print(text, flush=True)


def set_position(words: list[str]) -> dict:
    """
    Build the state that a "position" command describes.

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
    if words[1] == "startpos":
        state = state_from_fen(START_FEN)
    else:
        fen_end = words.index("moves") if "moves" in words else len(words)
        fen = ""
        for word in words[2:fen_end]:
            fen += word + " "
        state = state_from_fen(fen)
    if "moves" in words:
        for text in words[words.index("moves") + 1 :]:
            make_move(state, move_from_uci(text, state["turn"] == "w"))
    return state


def main():
    brain = BRAINS[sys.argv[1]] if len(sys.argv) > 1 else negamax_move
    state = state_from_fen(START_FEN)
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
            state = state_from_fen(START_FEN)
        elif command == "position":
            state = set_position(words)
        elif command == "go":
            if legal_moves(state):
                send(f"bestmove {move_to_uci(brain(state))}")
            else:
                send("bestmove 0000")
        elif command == "quit":
            break
        else:
            print(f"Remus ignores: {line.strip()}", file=sys.stderr)


if __name__ == "__main__":
    main()
