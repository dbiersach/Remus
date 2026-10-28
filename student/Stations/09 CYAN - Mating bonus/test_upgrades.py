"""test_upgrades.py

Tests for the CYAN station: the mating bonus.
"""

from evaluation import mating_bonus
from fen import state_from_fen
from search import MATE_SCORE

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_mating_bonus_prefers_the_losing_king_in_the_corner() -> None:
    corner = state_from_fen("7k/8/8/8/8/8/8/R3K3 w - - 0 1")["board"]
    center = state_from_fen("8/8/8/4k3/8/8/8/R3K3 w - - 0 1")["board"]
    level = state_from_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")["board"]
    assert mating_bonus(corner) > mating_bonus(center) > 0
    assert mating_bonus(level) == 0
