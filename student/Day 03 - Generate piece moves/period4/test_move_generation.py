"""test_move_generation.py

Tests for pseudo-legal move generation on small, hand-checked positions.
"""

from board import EMPTY, Board, parse_square, set_piece
from game_state import BLACK, WHITE, new_game
from move_generation import (
    BISHOP_DIRECTIONS,
    ROOK_DIRECTIONS,
    king_moves,
    knight_moves,
    pawn_captures,
    pawn_pushes,
    pseudo_legal_moves,
    slide,
    slider_moves,
)
from moves import move_to_uci


def empty_board() -> Board:
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


def test_rook_on_an_empty_board_has_14_moves() -> None:
    assert (
        len(slider_moves(empty_board(), parse_square("d4"), WHITE, ROOK_DIRECTIONS))
        == 14
    )


def test_bishop_on_c1_has_7_moves() -> None:
    assert (
        len(slider_moves(empty_board(), parse_square("c1"), WHITE, BISHOP_DIRECTIONS))
        == 7
    )


def test_slide_stops_at_a_friend_and_captures_an_enemy() -> None:
    board = empty_board()
    set_piece(board, parse_square("a1"), "R")
    set_piece(board, parse_square("a4"), "p")
    set_piece(board, parse_square("c1"), "B")
    assert targets(slide(board, parse_square("a1"), (-1, 0), WHITE)) == {
        "a2",
        "a3",
        "a4",
    }
    assert targets(slide(board, parse_square("a1"), (0, 1), WHITE)) == {"b1"}


def test_pawn_pushes_from_the_start_rank() -> None:
    board = new_game()["board"]
    assert targets(pawn_pushes(board, parse_square("e2"), WHITE)) == {"e3", "e4"}
    assert targets(pawn_pushes(board, parse_square("d7"), BLACK)) == {"d6", "d5"}


def test_blocked_pawn_has_no_pushes() -> None:
    board = empty_board()
    set_piece(board, parse_square("e2"), "P")
    set_piece(board, parse_square("e3"), "n")
    assert pawn_pushes(board, parse_square("e2"), WHITE) == []


def test_pawn_promotes_to_four_pieces() -> None:
    board = empty_board()
    set_piece(board, parse_square("b7"), "P")
    set_piece(board, parse_square("a8"), "r")
    moves = pawn_pushes(board, parse_square("b7"), WHITE) + pawn_captures(
        board, parse_square("b7"), WHITE
    )
    assert {move_to_uci(move) for move in moves} == {
        "b7b8q",
        "b7b8r",
        "b7b8b",
        "b7b8n",
        "b7a8q",
        "b7a8r",
        "b7a8b",
        "b7a8n",
    }


def test_twenty_moves_from_the_start() -> None:
    assert len(pseudo_legal_moves(new_game())) == 20
