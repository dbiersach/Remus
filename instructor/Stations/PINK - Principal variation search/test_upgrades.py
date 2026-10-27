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
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = pvs_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before
