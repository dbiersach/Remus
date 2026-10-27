"""test_move_generation.py

Tests for pseudo-legal move generation on small, hand-checked positions.
"""

from board import EMPTY, parse_square
from game_state import WHITE
from move_generation import king_moves, knight_moves
from moves import move_to_uci


def empty_board() -> list[list[str]]:
    return [[EMPTY] * 8 for _ in range(8)]


def targets(moves) -> set[str]:
    return {move_to_uci(move)[2:] for move in moves}


def test_knight_on_a1_has_two_moves() -> None:
    assert targets(knight_moves(empty_board(), parse_square("a1"), WHITE)) == {
        "b3",
        "c2",
    }


def test_knight_on_d4_has_eight_moves() -> None:
    assert len(knight_moves(empty_board(), parse_square("d4"), WHITE)) == 8


def test_king_in_the_corner_has_three_moves() -> None:
    assert targets(king_moves(empty_board(), parse_square("h1"), WHITE)) == {
        "g1",
        "g2",
        "h2",
    }
