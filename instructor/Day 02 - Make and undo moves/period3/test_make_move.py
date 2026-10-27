"""test_make_move.py

Tests for making and undoing quiet moves and captures.
"""

from board import EMPTY
from game_state import BLACK, WHITE, color_of
from moves import Move, move_from_uci, move_to_uci


def test_colors() -> None:
    assert color_of("K") == WHITE
    assert color_of("k") == BLACK
    assert color_of(EMPTY) is None


def test_uci_round_trip() -> None:
    for text in ["e2e4", "g8f6", "a7a8q", "h2h1n"]:
        assert move_to_uci(move_from_uci(text, white_to_move=text[3] == "8")) == text


def test_move_record_holds_squares() -> None:
    assert move_from_uci("e2e4") == Move((6, 4), (4, 4))
