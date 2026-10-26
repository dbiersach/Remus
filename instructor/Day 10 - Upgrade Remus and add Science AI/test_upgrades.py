"""test_upgrades.py

Tests for the Day 10 upgrade stations: pawn structure, the mating bonus, the
transposition table, killer moves, upgraded_search, the opening book, the mate
solver, and the hidden-peak Science AI.
"""

from evaluation import mating_bonus, pawn_structure
from fen import START_FEN, state_from_fen
from game_state import position_key
from hidden_peak import (
    PEAK,
    benchmark,
    candidate_squares,
    choose_next_measurement,
    make_grid,
    random_strategy,
)
from make_move import make_move, state_snapshot
from mate_solver import mating_move, read_puzzles
from moves import Move, move_from_uci, move_to_uci
from notation import move_to_san, parse_san
from opening_book import BOOK_PATH, book_move, load_book
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta_with_quiescence,
    remember_killer,
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
    info = SearchInfo()
    board = state_from_fen(START_FEN)["board"]
    for text in ("e2e4", "d2d4", "g1f3"):
        remember_killer(info, 2, move_from_uci(text), board)
    assert [move_to_uci(move) for move in info.killers[2]] == ["g1f3", "d2d4"]


def test_upgraded_search_agrees_with_alpha_beta() -> None:
    """The upgrades save work but find the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain = SearchInfo()
    upgraded = SearchInfo()
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, plain)
    upgraded_score, pv = upgraded_search(state, 3, 0, *WIDE, upgraded)
    assert upgraded_score == plain_score
    assert pv
    assert state_snapshot(state) == before


def test_upgraded_search_finds_a_mate_in_two() -> None:
    fen, best, _, _ = read_puzzles()[0]  # MATE.001: Be4
    state = state_from_fen(fen)
    score, pv = upgraded_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == MATE_SCORE - 3
    assert move_to_san(state, pv[0]) == best


def test_opening_book_is_legal_and_answers_e4() -> None:
    book = load_book()
    assert len(book) > 50
    state = state_from_fen(START_FEN)
    assert book_move(book, state) is not None
    make_move(state, parse_san(state, "e4"))
    assert move_to_uci(book_move(book, state)) in ("e7e5", "c7c5", "e7e6", "c7c6")


def test_missing_book_never_stops_play() -> None:
    book = load_book(BOOK_PATH.with_name("no_such_book.txt"))
    assert book == {}
    assert book_move(book, state_from_fen(START_FEN)) is None


def test_mate_solver_solves_all_gameworks_puzzles() -> None:
    """Ten puzzles: nine mates in 2 and MATE.008, a mate in 3."""
    puzzles = read_puzzles()
    assert len(puzzles) == 10
    for fen, best, length, name in puzzles:
        state = state_from_fen(fen)
        move = mating_move(state, length)
        assert move is not None, name
        assert move_to_san(state, move).rstrip("+#") == best, name


def test_mate_solver_finds_no_mate_when_there_is_none() -> None:
    assert mating_move(state_from_fen(START_FEN), 1) is None


def test_hidden_peak_grid_has_one_peak() -> None:
    grid = make_grid(7)
    assert sum(row.count(PEAK) for row in grid) == 1
    assert make_grid(7) == grid  # The same seed makes the same sample


def test_greedy_ai_measures_where_it_looks_hot() -> None:
    readings = {(5, 5): 10, (2, 2): 90}
    choice = choose_next_measurement(readings, explore_weight=0)
    assert choice in candidate_squares(readings)
    assert abs(choice[0] - 2) <= 1 and abs(choice[1] - 2) <= 1


def test_greedy_ai_beats_random_guessing() -> None:
    """Over 20 samples random guessing needs far more measurements than greedy."""
    assert benchmark(choose_next_measurement, 20) < benchmark(random_strategy, 20) / 2
