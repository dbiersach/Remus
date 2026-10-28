"""test_legal_moves.py

Tests for attacks, check, and the legal-move filter.
"""

from attacks import is_attacked_by_scanning, is_square_attacked
from board import EMPTY, parse_square, set_piece
from game_state import BLACK, WHITE, color_of, new_game


def position(pieces: dict[str, str], turn: str = WHITE) -> dict:
    """Build a state from {square name: piece}, with no castling rights."""
    state = new_game()
    state["board"] = [[EMPTY] * 8 for _ in range(8)]
    for name, piece in pieces.items():
        set_piece(state["board"], parse_square(name), piece)
    state["turn"] = turn
    state["castling"] = ""
    return state


def test_pawn_attacks_diagonally_forward() -> None:
    state = position({"e4": "P", "a1": "K", "h8": "k"})
    board = state["board"]
    assert is_square_attacked(board, parse_square("d5"), WHITE)
    assert is_square_attacked(board, parse_square("f5"), WHITE)
    assert not is_square_attacked(board, parse_square("e5"), WHITE)


def test_both_attack_checks_agree() -> None:
    state = position({"e4": "Q", "b2": "N", "g7": "p", "c6": "b", "a1": "K", "h8": "k"})
    board = state["board"]
    for row in range(8):
        for col in range(8):
            for color in (WHITE, BLACK):
                if color_of(board[row][col]) == color:
                    continue
                expected = is_attacked_by_scanning(board, (row, col), color)
                assert is_square_attacked(board, (row, col), color) == expected
