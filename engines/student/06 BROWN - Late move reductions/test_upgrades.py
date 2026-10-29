"""test_upgrades.py

Tests for the BROWN color version: late move reductions.
"""

from board import EMPTY
from fen import state_from_fen
from make_move import state_snapshot
from moves import Move
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    reduced_search,
    reduction,
)

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_only_late_quiet_moves_are_reduced() -> None:
    """Expected: only a late, quiet move with no check and 3 plies to go loses 1 ply."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError(
        "Day 9 P2: write test_only_late_quiet_moves_are_reduced()"
    )


def test_reduced_search_saves_work_and_keeps_the_state() -> None:
    """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError(
        "Day 9 P2: write test_reduced_search_saves_work_and_keeps_the_state()"
    )
