#!/usr/bin/env -S uv run
"""move_ordering.py

Put the moves most likely to be best first. Alpha-beta cuts off more of the tree
when it meets a strong move early, so a good order means fewer positions to visit.

Captures come first, ordered by MVV-LVA: Most Valuable Victim, Least Valuable
Attacker. Pawn takes queen comes before queen takes pawn.

Day 10 adds killer moves: a quiet move that caused a cutoff at some depth will
often cause one again in a sibling position, so it goes right after the captures.
"""

from board import EMPTY, Board, piece_at
from evaluation import PIECE_VALUES
from fen import state_from_fen
from legal_moves import legal_moves
from moves import Move, move_to_uci


def mvv_lva_score(move: Move, board: Board) -> int:
    """
    Score a move for ordering: high for a big capture by a small piece.

    Parameters
    ----------
    move : Move
        The move to score.
    board : Board
        The board before the move.

    Returns
    -------
    int
        0 for a quiet move. For a capture, ten times the victim's value minus the
        attacker's value, so any capture of a queen outranks any capture of a rook.
        A promotion counts like capturing the new piece.
    """
    victim = piece_at(board, move.to_square)
    attacker = piece_at(board, move.from_square)
    score = 0
    if victim != EMPTY:
        score = 10 * PIECE_VALUES[victim.upper()] - PIECE_VALUES[attacker.upper()]
    if move.promotion is not None:
        score += 10 * PIECE_VALUES[move.promotion.upper()]
    return score


KILLER_SCORE = 50  # Ranks a killer move above quiet moves and below every capture


def order_moves(
    moves: list[Move],
    board: Board,
    first: Move | None = None,
    killers: list[Move] | None = None,
) -> list[Move]:
    """
    Return the moves sorted best first.

    Parameters
    ----------
    moves : list[Move]
        The moves to order.
    board : Board
        The board before the moves.
    first : Move | None
        A move to try before all others, such as the best move from the previous,
        shallower search.
    killers : list[Move] | None
        Quiet moves that caused cutoffs at this depth in other positions.

    Returns
    -------
    list[Move]
        The moves, highest MVV-LVA score first, killers after the captures, with
        `first` at the front.
    """
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write order_moves()")


def main():
    state = state_from_fen("4k3/8/2q5/1P1r4/8/8/8/3QK3 w - - 0 1")
    ordered = order_moves(legal_moves(state), state["board"])
    print(f"First two moves: {move_to_uci(ordered[0])} {move_to_uci(ordered[1])}")
    print("  (expected b5c6, pawn takes queen, then d1d5, queen takes rook)")


if __name__ == "__main__":
    main()
