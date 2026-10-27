"""test_upgrades.py

Tests for the YELLOW station: draw sense.
"""

from fen import START_FEN, state_from_fen
from make_move import make_move, state_snapshot
from moves import move_from_uci
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    draw_sense_search,
    is_draw_in_search,
)

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_draw_sense_search_agrees_with_alpha_beta() -> None:
    """The station saves work but finds the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = draw_sense_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before


def test_a_repeated_position_is_a_draw() -> None:
    """After Nf3 Nf6 Ng1 Ng8 the starting position appears for the second time."""
    state = state_from_fen(START_FEN)
    assert not is_draw_in_search(state)
    for text in ("g1f3", "g8f6", "f3g1", "f6g8"):
        make_move(state, move_from_uci(text))
    assert is_draw_in_search(state)


def test_the_fifty_move_limit_is_a_draw() -> None:
    state = state_from_fen("4k3/8/8/8/8/8/8/R3K3 w - - 100 80")
    assert is_draw_in_search(state)
