#!/usr/bin/env -S uv run
"""move_ordering.py

Put the moves most likely to be best first. Alpha-beta cuts off more of the tree
when it meets a strong move early, so a good order means fewer positions to visit.

Captures come first, ordered by MVV-LVA: Most Valuable Victim, Least Valuable
Attacker. Pawn takes queen comes before queen takes pawn.
"""

from board import EMPTY, piece_at
from evaluation import PIECE_VALUES
from fen import state_from_fen
from legal_moves import legal_moves
from moves import Move, move_to_uci


def mvv_lva_score(move: Move, board: list[list[str]]) -> int:
    """
    Score a move for ordering: high for a big capture by a small piece.

    Parameters
    ----------
    move : Move
        The move to score.
    board : list[list[str]]
        The board before the move.

    Returns
    -------
    int
        0 for a quiet move. For a capture, ten times the victim's value minus the
        attacker's value, so any capture of a queen outranks any capture of a rook.
        A promotion counts like capturing the new piece.
    """
    # Day 8, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 8 P4: write mvv_lva_score()")


def order_moves(
    moves: list[Move], board: list[list[str]], first: Move | None = None
) -> list[Move]:
    """
    Return the moves sorted best first.

    Parameters
    ----------
    moves : list[Move]
        The moves to order.
    board : list[list[str]]
        The board before the moves.
    first : Move | None
        A move to try before all others, such as the best move from the previous,
        shallower search.

    Returns
    -------
    list[Move]
        The moves, highest MVV-LVA score first, with `first` at the front.
    """
    ordered = []
    scores = []
    for move in moves:
        score = mvv_lva_score(move, board)
        # Step past every move that scores at least as high, so ties keep their order
        place = 0
        while place < len(scores) and scores[place] >= score:
            place += 1
        ordered.insert(place, move)
        scores.insert(place, score)
    if first in ordered:
        ordered.remove(first)
        ordered.insert(0, first)
    return ordered


def main():
    state = state_from_fen("4k3/8/2q5/1P1r4/8/8/8/3QK3 w - - 0 1")
    ordered = order_moves(legal_moves(state), state["board"])
    print(f"First two moves: {move_to_uci(ordered[0])} {move_to_uci(ordered[1])}")
    print("  (expected b5c6, pawn takes queen, then d1d5, queen takes rook)")


if __name__ == "__main__":
    main()
