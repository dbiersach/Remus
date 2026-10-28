"""test_make_move.py

Tests for making and undoing quiet moves and captures.
"""

from board import EMPTY, parse_square, piece_at
from game_state import BLACK, WHITE, color_of, new_game
from make_move import make_move, state_snapshot, undo_move
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


def test_e2e4_changes_board_and_turn() -> None:
    state = new_game()
    make_move(state, move_from_uci("e2e4"))
    assert piece_at(state["board"], parse_square("e4")) == "P"
    assert piece_at(state["board"], parse_square("e2")) == EMPTY
    assert state["turn"] == BLACK
    assert state["halfmove_clock"] == 0


def test_knight_move_counts_toward_fifty_moves() -> None:
    state = new_game()
    make_move(state, move_from_uci("g1f3"))
    assert state["halfmove_clock"] == 1


def test_capture_and_undo() -> None:
    state = new_game()
    for text in ["e2e4", "d7d5"]:
        make_move(state, move_from_uci(text))
    before = state_snapshot(state)
    undo = make_move(state, move_from_uci("e4d5"))
    assert piece_at(state["board"], parse_square("d5")) == "P"
    undo_move(state, undo)
    assert state_snapshot(state) == before


def test_ten_moves_made_and_undone_return_the_start() -> None:
    state = new_game()
    start = state_snapshot(state)
    texts = [
        "e2e4",
        "e7e5",
        "g1f3",
        "b8c6",
        "f1b5",
        "a7a6",
        "b5c6",
        "d7c6",
        "e1f1",
        "g8f6",
    ]
    records = [make_move(state, move_from_uci(text)) for text in texts]
    assert state["fullmove_number"] == 6
    for undo in reversed(records):
        undo_move(state, undo)
    assert state_snapshot(state) == start
