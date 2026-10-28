"""test_upgrades.py

Tests for the ten enhancements of Remus-GOLD: pawn structure, the mating bonus, king
safety, the transposition table, killer moves, null moves, late move reductions,
upgraded_search, and the opening book.
"""

from board import EMPTY
from evaluation import king_safety, mating_bonus, pawn_structure
from fen import START_FEN, state_from_fen
from game_state import position_key
from make_move import make_move, state_snapshot
from mate_solver import read_puzzles
from moves import Move, move_from_uci, move_to_uci
from notation import move_to_san, parse_san
from opening_book import BOOK_PATH, book_move, load_book
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    make_null_move,
    reduction,
    remember_killer,
    undo_null_move,
    upgraded_search,
)
from transposition_table import EXACT, LOWER, UPPER, best_stored_move, probe, store

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_pawn_structure_is_level_at_the_start() -> None:
    assert pawn_structure(state_from_fen(START_FEN)["board"]) == 0


def test_doubled_isolated_pawns_cost_points() -> None:
    """White's two pawns on the e-file are doubled and isolated: worse than Black's."""
    board = state_from_fen("4k3/3ppp2/8/8/8/4P3/4P3/4K3 w - - 0 1")["board"]
    assert pawn_structure(board) < 0


def test_a_passed_pawn_earns_a_bonus() -> None:
    board = state_from_fen("4k3/8/1P6/8/8/8/8/4K3 w - - 0 1")["board"]
    assert pawn_structure(board) > 0


def test_mating_bonus_prefers_the_losing_king_in_the_corner() -> None:
    corner = state_from_fen("7k/8/8/8/8/8/8/R3K3 w - - 0 1")["board"]
    center = state_from_fen("8/8/8/4k3/8/8/8/R3K3 w - - 0 1")["board"]
    level = state_from_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")["board"]
    assert mating_bonus(corner) > mating_bonus(center) > 0
    assert mating_bonus(level) == 0


def test_transposition_table_bounds() -> None:
    """Expected: an exact entry answers at its depth; a bound answers only when it
    settles the window."""
    table = {}
    best = Move((6, 4), (4, 4))
    store(table, "a", 3, 50, EXACT, best)
    store(table, "b", 3, 80, LOWER, None)
    store(table, "c", 3, -20, UPPER, None)
    assert probe(table, "a", 3, -100, 100) == 50
    assert probe(table, "a", 4, -100, 100) is None  # Not searched deep enough
    assert probe(table, "b", 3, -100, 70) == 80  # At least 80 is a cutoff above beta 70
    assert (
        probe(table, "b", 3, -100, 100) is None
    )  # At least 80 does not settle beta 100
    assert probe(table, "c", 3, 0, 100) == -20  # At most -20 cannot beat alpha 0
    assert best_stored_move(table, "a") == best


def test_two_move_orders_reach_one_position_key() -> None:
    first = state_from_fen(START_FEN)
    second = state_from_fen(START_FEN)
    for text in ("g1f3", "g8f6", "b1c3"):
        make_move(first, move_from_uci(text))
    for text in ("b1c3", "g8f6", "g1f3"):
        make_move(second, move_from_uci(text))
    assert position_key(first) == position_key(second)


def test_killers_keep_two_quiet_moves() -> None:
    """Expected: after three cutoffs at ply 2, the two newest moves stay, newest first."""
    info = SearchInfo()
    board = state_from_fen(START_FEN)["board"]
    for text in ("e2e4", "d2d4", "g1f3"):
        remember_killer(info, 2, move_from_uci(text), board)
    assert [move_to_uci(move) for move in info.killers[2]] == ["g1f3", "d2d4"]


def test_king_safety_rewards_the_pawn_shield() -> None:
    """Three pawns in front of the castled White king earn 3 * 15 = 45."""
    sheltered = state_from_fen("q3k3/8/8/8/8/8/5PPP/6K1 w - - 0 1")["board"]
    no_queen = state_from_fen("4k3/8/8/8/8/8/5PPP/6K1 w - - 0 1")["board"]
    assert king_safety(sheltered) == 45
    assert king_safety(no_queen) == 0  # Without the enemy queen the term is off
    assert king_safety(state_from_fen(START_FEN)["board"]) == 0


def test_null_move_and_undo_restore_the_state() -> None:
    """Expected: a pass gives Black the turn, and its undo restores the exact state."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    en_passant = make_null_move(state)
    assert state["turn"] == "b"
    undo_null_move(state, en_passant)
    assert state_snapshot(state) == before


def test_only_late_quiet_moves_are_reduced() -> None:
    """Expected: only a late, quiet move with no check and 3 plies to go loses 1 ply."""
    quiet = Move((6, 0), (5, 0))
    assert reduction(4, 5, quiet, EMPTY, False) == 1
    assert reduction(4, 1, quiet, EMPTY, False) == 0  # Early in the list
    assert reduction(2, 5, quiet, EMPTY, False) == 0  # Too close to the leaves
    assert reduction(4, 5, quiet, "p", False) == 0  # A capture
    assert reduction(4, 5, quiet, EMPTY, True) == 0  # A check


def test_upgraded_search_saves_work_and_keeps_the_state() -> None:
    """The upgrades search fewer positions than plain alpha-beta at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain = SearchInfo()
    upgraded = SearchInfo()
    alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
    _, pv = upgraded_search(state, 4, 0, *WIDE, upgraded)
    assert upgraded.nodes < plain.nodes
    assert pv
    assert state_snapshot(state) == before


def test_upgraded_search_finds_a_mate_in_two() -> None:
    """Be4 is a quiet move late in the list, so late move reductions first search it
    two plies shallower; depth 5 leaves room to prove the mate in 3 plies."""
    fen, best, _, _ = read_puzzles()[0]  # MATE.001: Be4
    state = state_from_fen(fen)
    score, pv = upgraded_search(state, 5, 0, *WIDE, SearchInfo())
    assert score == MATE_SCORE - 3
    assert move_to_san(state, pv[0]) == best


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
