"""test_upgrades.py

Tests for the GREEN station: the opening book.
"""

from fen import START_FEN, state_from_fen
from make_move import make_move
from moves import move_to_uci
from notation import parse_san
from opening_book import BOOK_PATH, book_move, load_book
from search import MATE_SCORE

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_opening_book_is_legal_and_answers_e4() -> None:
    book = load_book()
    assert len(book) > 50
    state = state_from_fen(START_FEN)
    assert book_move(book, state) is not None
    make_move(state, parse_san(state, "e4"))
    reply = book_move(book, state)
    assert reply is not None
    assert move_to_uci(reply) in ("e7e5", "c7c5", "e7e6", "c7c6")


def test_book_typo_is_skipped_without_touching_stdout(tmp_path, capsys) -> None:
    """A bad move ends its line; the report goes to stderr, never into the UCI stream."""
    file_path = tmp_path / "typo_book.txt"
    file_path.write_text("e4 e5 Nf9 Nc6\n")
    book = load_book(file_path)
    assert len(book) == 2  # The start position and the position after 1. e4
    output = capsys.readouterr()
    assert output.out == ""
    assert "Nf9" in output.err


def test_missing_book_never_stops_play() -> None:
    book = load_book(BOOK_PATH.with_name("no_such_book.txt"))
    assert book == {}
    assert book_move(book, state_from_fen(START_FEN)) is None
