#!/usr/bin/env -S uv run
"""search.py

Choose a move. Remus's first two "brains" are simple: a random legal move, and a
greedy move that grabs the most valuable piece it can capture.
"""

import random

from board import EMPTY, piece_at
from fen import state_from_fen
from legal_moves import legal_moves
from moves import Move, move_to_uci

PIECE_VALUES = {
    "P": 100,
    "N": 300,
    "B": 300,
    "R": 500,
    "Q": 900,
    "K": 0,
}  # In centipawns


def random_move(state: dict) -> Move:
    """Return a random legal move."""
    # Day 7, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 7 P3: write random_move()")


def capture_value(state: dict, move: Move) -> int:
    """Return the value of the piece a move captures, or 0 for a quiet move."""
    captured = piece_at(state["board"], move.to_square)
    if captured == EMPTY:
        return 0
    return PIECE_VALUES[captured.upper()]


def greedy_move(state: dict) -> Move:
    """
    Return the move that captures the most valuable piece.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    Move
        The capture of the most valuable piece. When no move captures anything,
        a random legal move.
    """
    # Day 7, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 7 P3: write greedy_move()")


def main():
    state = state_from_fen("4k3/8/8/3q4/8/2N1p3/8/4K3 w - - 0 1")
    print(
        f"Greedy move: {move_to_uci(greedy_move(state))}  (expected c3d5, taking the queen)"
    )
    print(f"Random move: {move_to_uci(random_move(state))}  (any legal move)")


if __name__ == "__main__":
    main()
