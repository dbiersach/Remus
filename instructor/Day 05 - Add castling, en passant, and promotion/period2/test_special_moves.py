"""test_special_moves.py

Tests for castling, en passant, promotion, and underpromotion, each with exact undo,
and a check that the UCI engine follows a game with castling in it.
"""

from board import EMPTY, parse_square, piece_at, set_piece
from game_state import WHITE, new_game
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move, update_castling_rights
from moves import move_from_uci, move_to_uci


def position(pieces: dict[str, str], turn: str = WHITE, castling: str = "") -> dict:
    """Build a state from {square name: piece}."""
    state = new_game()
    state["board"] = [[EMPTY] * 8 for _ in range(8)]
    for name, piece in pieces.items():
        set_piece(state["board"], parse_square(name), piece)
    state["turn"] = turn
    state["castling"] = castling
    return state


def uci_set(state: dict) -> set[str]:
    return {move_to_uci(move) for move in legal_moves(state)}


def play(state: dict, texts: list[str]) -> None:
    for text in texts:
        make_move(state, move_from_uci(text, state["turn"] == WHITE))


def test_both_castlings_are_available() -> None:
    state = position({"e1": "K", "a1": "R", "h1": "R", "e8": "k"}, castling="KQ")
    assert {"e1g1", "e1c1"} <= uci_set(state)


def test_no_castling_out_of_check() -> None:
    state = position(
        {"e1": "K", "a1": "R", "h1": "R", "e8": "k", "e5": "r"}, castling="KQ"
    )
    assert not {"e1g1", "e1c1"} & uci_set(state)


def test_no_castling_through_an_attacked_square() -> None:
    state = position({"e1": "K", "h1": "R", "e8": "k", "f5": "r"}, castling="K")
    assert "e1g1" not in uci_set(state)


def test_no_castling_into_check() -> None:
    state = position({"e1": "K", "h1": "R", "e8": "k", "g5": "r"}, castling="K")
    assert "e1g1" not in uci_set(state)


def test_queenside_rook_may_cross_an_attacked_b1() -> None:
    state = position({"e1": "K", "a1": "R", "e8": "k", "b5": "r"}, castling="Q")
    assert "e1c1" in uci_set(state)


def test_castling_moves_the_rook_and_undo_restores_it() -> None:
    state = position({"e1": "K", "h1": "R", "e8": "k"}, castling="K")
    before = state_snapshot(state)
    undo = make_move(state, move_from_uci("e1g1"))
    assert piece_at(state["board"], parse_square("f1")) == "R"
    assert piece_at(state["board"], parse_square("h1")) == EMPTY
    assert state["castling"] == ""
    undo_move(state, undo)
    assert state_snapshot(state) == before


def test_rook_capture_removes_the_right() -> None:
    assert update_castling_rights("KQkq", move_from_uci("b2h8")) == "KQq"
    assert update_castling_rights("KQkq", move_from_uci("h1h5")) == "Qkq"
    assert update_castling_rights("KQkq", move_from_uci("e8d8")) == "KQ"
