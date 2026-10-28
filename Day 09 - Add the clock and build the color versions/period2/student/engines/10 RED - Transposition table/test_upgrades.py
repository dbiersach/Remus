"""test_upgrades.py

Tests for the RED color version: the transposition table and table_search.
"""

from fen import START_FEN, state_from_fen
from game_state import position_key
from make_move import make_move, state_snapshot
from moves import Move, move_from_uci
from search import MATE_SCORE, SearchInfo, alpha_beta_with_quiescence, table_search
from transposition_table import EXACT, LOWER, UPPER, best_stored_move, probe, store

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_transposition_table_bounds() -> None:
    """Expected: an exact entry answers at its depth; a bound answers only when it
    settles the window."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError("Day 9 P2: write test_transposition_table_bounds()")


def test_two_move_orders_reach_one_position_key() -> None:
    first = state_from_fen(START_FEN)
    second = state_from_fen(START_FEN)
    for text in ("g1f3", "g8f6", "b1c3"):
        make_move(first, move_from_uci(text))
    for text in ("b1c3", "g8f6", "g1f3"):
        make_move(second, move_from_uci(text))
    assert position_key(first) == position_key(second)


def test_table_search_agrees_with_alpha_beta() -> None:
    """The color version saves work but finds the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = table_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before
