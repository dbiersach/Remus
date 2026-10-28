"""test_upgrades.py

Tests for the YELLOW color version: draw sense.
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
    """The color version saves work but finds the same score at the same depth."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError(
        "Day 9 P2: write test_draw_sense_search_agrees_with_alpha_beta()"
    )


def test_a_repeated_position_is_a_draw() -> None:
    """After Nf3 Nf6 Ng1 Ng8 the starting position appears for the second time."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError("Day 9 P2: write test_a_repeated_position_is_a_draw()")


def test_the_fifty_move_limit_is_a_draw() -> None:
    """A halfmove clock of 100 is 50 moves by each side with no capture or pawn move."""
    # Day 9, period 2: write this function.
    # The docstring above says what this test must check.
    raise NotImplementedError("Day 9 P2: write test_the_fifty_move_limit_is_a_draw()")
