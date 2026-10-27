"""test_upgrades.py

Tests for the PINK station: principal variation search.
"""

from fen import state_from_fen
from make_move import state_snapshot
from search import MATE_SCORE, SearchInfo, alpha_beta_with_quiescence, pvs_search

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_pvs_search_agrees_with_alpha_beta() -> None:
    """The station saves work but finds the same score at the same depth."""
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write test_pvs_search_agrees_with_alpha_beta()")


def test_a_null_window_answers_only_better_or_not() -> None:
    """A null window (alpha, alpha + 1) says only whether the exact score beats alpha."""
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write test_a_null_window_answers_only_better_or_not()")
