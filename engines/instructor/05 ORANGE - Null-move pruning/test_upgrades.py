"""test_upgrades.py

Tests for Remus-ORANGE: null-move pruning.
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
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    en_passant = make_null_move(state)
    assert state["turn"] == "b"
    undo_null_move(state, en_passant)
    assert state_snapshot(state) == before


def test_null_move_search_saves_work_and_keeps_the_state() -> None:
    """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain = SearchInfo()
    upgraded = SearchInfo()
    alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
    _, pv = null_move_search(state, 4, 0, *WIDE, upgraded)
    assert upgraded.nodes < plain.nodes
    assert pv
    assert state_snapshot(state) == before
