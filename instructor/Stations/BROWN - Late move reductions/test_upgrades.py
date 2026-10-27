"""test_upgrades.py

Tests for the BROWN station: late move reductions.
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
    quiet = Move((6, 0), (5, 0))
    assert reduction(4, 5, quiet, EMPTY, False) == 1
    assert reduction(4, 1, quiet, EMPTY, False) == 0  # Early in the list
    assert reduction(2, 5, quiet, EMPTY, False) == 0  # Too close to the leaves
    assert reduction(4, 5, quiet, "p", False) == 0  # A capture
    assert reduction(4, 5, quiet, EMPTY, True) == 0  # A check


def test_reduced_search_saves_work_and_keeps_the_state() -> None:
    """The station searches fewer positions than plain alpha-beta at depth 4."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain = SearchInfo()
    station = SearchInfo()
    alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
    _, pv = reduced_search(state, 4, 0, *WIDE, station)
    assert station.nodes < plain.nodes
    assert pv
    assert state_snapshot(state) == before
