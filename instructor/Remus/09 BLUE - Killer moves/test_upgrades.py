"""test_upgrades.py

Tests for the BLUE color version: killer moves and killer_search.
"""

from fen import START_FEN, state_from_fen
from make_move import state_snapshot
from moves import move_from_uci, move_to_uci
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    killer_search,
    remember_killer,
)

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_killers_keep_two_quiet_moves() -> None:
    """Expected: after three cutoffs at ply 2, the two newest moves stay, newest first."""
    info = SearchInfo()
    board = state_from_fen(START_FEN)["board"]
    for text in ("e2e4", "d2d4", "g1f3"):
        remember_killer(info, 2, move_from_uci(text), board)
    assert [move_to_uci(move) for move in info.killers[2]] == ["g1f3", "d2d4"]


def test_killer_search_agrees_with_alpha_beta() -> None:
    """The color version saves work but finds the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = killer_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before
