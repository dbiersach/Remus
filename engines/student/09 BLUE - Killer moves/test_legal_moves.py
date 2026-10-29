"""test_legal_moves.py

Tests for attacks, check, and the legal-move filter.
"""

from attacks import in_check, is_attacked_by_scanning, is_square_attacked
from board import EMPTY, parse_square, set_piece
from game_state import BLACK, WHITE, color_of, new_game
from legal_moves import legal_moves
from make_move import state_snapshot
from moves import move_to_uci


def position(pieces: dict[str, str], turn: str = WHITE) -> dict:
    """Build a state from {square name: piece}, with no castling rights."""
    state = new_game()
    state["board"] = [[EMPTY] * 8 for _ in range(8)]
    for name, piece in pieces.items():
        set_piece(state["board"], parse_square(name), piece)
    state["turn"] = turn
    state["castling"] = ""
    return state


def test_twenty_legal_moves_from_the_start() -> None:
    assert len(legal_moves(new_game())) == 20


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


def test_rook_check() -> None:
    state = position({"e1": "K", "e8": "r", "a8": "k"})
    assert in_check(state, WHITE)


def test_pinned_knight_has_no_moves() -> None:
    state = position({"e1": "K", "e2": "N", "e8": "r", "a8": "k"})
    knight_moves = [m for m in legal_moves(state) if move_to_uci(m).startswith("e2")]
    assert knight_moves == []


def test_king_in_check_has_only_escapes() -> None:
    state = position({"e1": "K", "e8": "r", "a8": "k", "a2": "P"})
    moves = {move_to_uci(m) for m in legal_moves(state)}
    assert moves == {"e1d1", "e1d2", "e1f1", "e1f2"}


def test_king_cannot_step_next_to_the_other_king() -> None:
    state = position({"e1": "K", "e3": "k"}, turn=WHITE)
    moves = {move_to_uci(m) for m in legal_moves(state)}
    assert moves == {"e1d1", "e1f1"}


def test_legal_moves_leave_the_state_unchanged() -> None:
    state = position({"e1": "K", "e2": "N", "e8": "r", "a8": "k"})
    before = state_snapshot(state)
    legal_moves(state)
    assert state_snapshot(state) == before
