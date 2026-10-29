"""test_upgrades.py

Tests for Remus-PURPLE: pawn structure.
"""

from evaluation import pawn_structure
from fen import START_FEN, state_from_fen
from search import MATE_SCORE

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_pawn_structure_is_level_at_the_start() -> None:
    assert pawn_structure(state_from_fen(START_FEN)["board"]) == 0


def test_doubled_isolated_pawns_cost_points() -> None:
    """White's two pawns on the e-file are doubled and isolated: worse than Black's."""
    board = state_from_fen("4k3/3ppp2/8/8/8/4P3/4P3/4K3 w - - 0 1")["board"]
    assert pawn_structure(board) < 0


def test_a_passed_pawn_earns_a_bonus() -> None:
    board = state_from_fen("4k3/8/1P6/8/8/8/8/4K3 w - - 0 1")["board"]
    assert pawn_structure(board) > 0
