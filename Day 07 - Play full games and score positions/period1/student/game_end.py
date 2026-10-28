#!/usr/bin/env -S uv run
"""game_end.py

Decide whether the game is over, and why: checkmate, stalemate, insufficient
material, repetition, or the fifty-move rule.

Threefold repetition and the fifty-move rule let a player claim a draw. Remus
treats them as the end of the game, the way chess GUIs and engine tournaments do.
"""

from attacks import in_check
from board import EMPTY, Board
from fen import state_from_fen
from legal_moves import legal_moves


def insufficient_material(board: Board) -> bool:
    """
    Return True if neither side can ever checkmate.

    Parameters
    ----------
    board : Board
        The board.

    Returns
    -------
    bool
        True for king against king, king and bishop against king, king and knight
        against king, and kings with bishops that all stand on squares of one color.
    """
    # Day 7, period 1: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 7 P1: write insufficient_material()")


def repetition_count(state: dict) -> int:
    """Return how many times the current position has appeared in the game."""
    return state["history"].count(state["history"][-1])


def game_result(state: dict) -> tuple[str, str] | None:
    """
    Return the result and the reason if the game is over, or None if it goes on.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    tuple[str, str] | None
        A result ("1-0", "0-1", or "1/2-1/2") and a reason, such as
        ("1-0", "checkmate").
    """
    # Day 7, period 1: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 7 P1: write game_result()")


def main():
    positions = [
        (
            "Fool's mate",
            "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3",
        ),
        ("Stalemate", "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"),
        ("King and knight", "8/8/4k3/8/8/2N5/8/4K3 w - - 0 1"),
        ("Start", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
    ]
    for name, fen in positions:
        print(f"{name}: {game_result(state_from_fen(fen))}")
    print(
        "  (expected 0-1 checkmate, a stalemate draw, an insufficient material draw, None)"
    )


if __name__ == "__main__":
    main()
