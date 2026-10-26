"""test_board.py

Tests for the board and its coordinates. Row 0 is rank 8 and column 0 is file a.
"""

import pytest
from board import EMPTY, new_board, parse_square, piece_at, square_name


def test_e2_is_row_6_col_4() -> None:
    assert parse_square("e2") == (6, 4)


def test_corners_round_trip() -> None:
    for name in ["a8", "h8", "a1", "h1"]:
        assert square_name(*parse_square(name)) == name


def test_every_square_round_trips() -> None:
    for row in range(8):
        for col in range(8):
            assert parse_square(square_name(row, col)) == (row, col)


def test_bad_square_names_are_rejected() -> None:
    for name in ["i9", "e0", "e", "e22", ""]:
        with pytest.raises(ValueError):
            parse_square(name)


def test_start_position_pieces() -> None:
    board = new_board()
    assert piece_at(board, parse_square("e1")) == "K"
    assert piece_at(board, parse_square("d8")) == "q"
    assert piece_at(board, parse_square("b1")) == "N"
    assert piece_at(board, parse_square("e4")) == EMPTY


def test_new_board_rows_are_separate_lists() -> None:
    """Changing one square must not change any other square."""
    board = new_board()
    board[6][4] = EMPTY
    assert board[6][3] == "P"
    assert new_board()[6][4] == "P"
