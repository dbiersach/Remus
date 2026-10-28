"""test_upgrades.py

Tests for the GRAY station: king safety.
"""

from evaluation import king_safety
from fen import START_FEN, state_from_fen
from search import MATE_SCORE

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_king_safety_rewards_the_pawn_shield() -> None:
    """Three pawns in front of the castled White king earn 3 * 15 = 45."""
    sheltered = state_from_fen("q3k3/8/8/8/8/8/5PPP/6K1 w - - 0 1")["board"]
    no_queen = state_from_fen("4k3/8/8/8/8/8/5PPP/6K1 w - - 0 1")["board"]
    assert king_safety(sheltered) == 45
    assert king_safety(no_queen) == 0  # Without the enemy queen the term is off
    assert king_safety(state_from_fen(START_FEN)["board"]) == 0
