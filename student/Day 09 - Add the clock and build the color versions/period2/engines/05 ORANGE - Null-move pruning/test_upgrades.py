"""test_upgrades.py

Tests for the ORANGE color version: null-move pruning.
"""

from fen import state_from_fen
from make_move import state_snapshot
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    make_null_move,
    null_move_search,
    undo_null_move,
)

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_null_move_and_undo_restore_the_state() -> None:
    """Expected: a pass gives Black the turn, and its undo restores the exact state."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError(
        "Day 9 P2: write test_null_move_and_undo_restore_the_state()"
    )


def test_null_move_search_saves_work_and_keeps_the_state() -> None:
    """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError(
        "Day 9 P2: write test_null_move_search_saves_work_and_keeps_the_state()"
    )
