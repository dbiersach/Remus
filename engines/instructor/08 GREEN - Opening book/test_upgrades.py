"""test_upgrades.py

Tests for the GREEN color version: the opening book.
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
    # The book answers 1. e4 with e5, c5, e6, c6, d6, d5, or Nf6
    replies = ("e7e5", "c7c5", "e7e6", "c7c6", "d7d6", "d7d5", "g8f6")
    assert move_to_uci(reply) in replies


def test_book_typo_is_skipped_without_touching_stdout(tmp_path, capsys) -> None:
    """A bad move ends its line; the report goes to stderr, never into the UCI stream."""
    file_path = tmp_path / "typo_book.txt"
    file_path.write_text("e4 e5 Nf9 Nc6\n")
    book = load_book(file_path)
    assert len(book) == 2  # The start position and the position after 1. e4
    output = capsys.readouterr()
    assert output.out == ""
    assert "Nf9" in output.err


def test_trap_line_stores_only_the_defenders_moves(tmp_path) -> None:
    """A "Black:" line teaches Black's defense and never White's trap."""
    file_path = tmp_path / "trap_book.txt"
    file_path.write_text("Black: e4 e5 Bc4 Nc6 Qh5 g6\n")
    book = load_book(file_path)
    assert len(book) == 3  # After 1. e4, after 2. Bc4, and after 3. Qh5
    state = state_from_fen(START_FEN)
    assert book_move(book, state) is None  # White's 1. e4 is not stored
    make_move(state, parse_san(state, "e4"))
    reply = book_move(book, state)
    assert reply is not None
    assert move_to_uci(reply) == "e7e5"


def test_book_answers_scholars_mate_but_never_tries_it() -> None:
    book = load_book()
    state = state_from_fen(START_FEN)
    for text in ("e4", "e5", "Bc4", "Nc6"):
        make_move(state, parse_san(state, text))
    assert book_move(book, state) is None  # White never plays 3. Qh5 from the book
    make_move(state, parse_san(state, "Qh5"))
    reply = book_move(book, state)
    assert reply is not None
    assert move_to_uci(reply) == "g7g6"


def test_missing_book_never_stops_play() -> None:
    book = load_book(BOOK_PATH.with_name("no_such_book.txt"))
    assert book == {}
    assert book_move(book, state_from_fen(START_FEN)) is None
