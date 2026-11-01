"""test_platinum.py

Tests for the Remus-PLATINUM additions: tapered evaluation, the pawn race,
mobility, the bishop pair, rooks on open files, static exchange evaluation,
delta and futility pruning, aspiration windows, and time management.
"""

import time

from evaluation import (
    BISHOP_PAIR,
    ROOK_HALF_OPEN_FILE,
    ROOK_OPEN_FILE,
    TOTAL_PHASE,
    UNSTOPPABLE_PAWN,
    game_phase,
    mobility,
    pawn_race,
    piece_terms,
    taper,
    tapered_terms,
)
from exchange import static_exchange
from fen import START_FEN, state_from_fen
from make_move import state_snapshot
from moves import Move, move_to_uci
from search import (
    MATE_SCORE,
    SearchInfo,
    aspiration_search,
    quiescence,
    think,
    upgraded_search,
)
from uci_engine import longest_time, thinking_time

WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


def test_phase_runs_from_full_to_zero() -> None:
    assert game_phase(state_from_fen(START_FEN)["board"]) == TOTAL_PHASE
    pawns_only = state_from_fen("4k3/pppp4/8/8/8/8/PPPP4/4K3 w - - 0 1")
    assert game_phase(pawns_only["board"]) == 0


def test_taper_blends_the_two_scores() -> None:
    """Expected: all middlegame at 24, all endgame at 0, halfway at 12."""
    assert taper(10, 50, 24) == 10
    assert taper(10, 50, 0) == 50
    assert taper(10, 50, 12) == 30


def test_endgame_king_prefers_the_center() -> None:
    center = state_from_fen("4k3/8/8/8/4K3/8/8/8 w - - 0 1")["board"]
    corner = state_from_fen("4k3/8/8/8/8/8/8/K7 w - - 0 1")["board"]
    assert tapered_terms(center) > tapered_terms(corner)


def test_start_position_terms_are_level() -> None:
    board = state_from_fen(START_FEN)["board"]
    assert tapered_terms(board) == 0
    assert mobility(board) == 0
    assert piece_terms(board) == 0


def test_pawn_race_rule_of_the_square() -> None:
    """e5 pawn, 3 moves from e8. Black king a5 is 4 steps away: unstoppable with
    White to move. With Black to move the king gains a step, 3, and catches it."""
    state = state_from_fen("8/8/8/k3P3/8/8/8/4K3 w - - 0 1")
    assert pawn_race(state["board"], "w") == UNSTOPPABLE_PAWN
    assert pawn_race(state["board"], "b") == 0


def test_pawn_race_needs_a_pawn_ending() -> None:
    """A Black knight can stop the pawn, so the race term is 0."""
    board = state_from_fen("8/8/8/k3P3/8/8/8/n3K3 w - - 0 1")["board"]
    assert pawn_race(board, "w") == 0


def test_knight_mobility() -> None:
    """A knight on e4 of an otherwise empty board reaches 8 squares: 8 * 4 = 32."""
    board = state_from_fen("k7/8/8/8/4N3/8/8/7K w - - 0 1")["board"]
    assert mobility(board) == 32


def test_bishop_pair_and_open_files() -> None:
    pair = state_from_fen("4k3/8/8/8/8/8/8/2B1KB2 w - - 0 1")["board"]
    assert piece_terms(pair) == BISHOP_PAIR
    open_file = state_from_fen("4k3/p7/8/8/8/8/8/3RK3 w - - 0 1")["board"]
    assert piece_terms(open_file) == ROOK_OPEN_FILE
    half_open = state_from_fen("3pk3/8/8/8/8/8/8/3RK3 w - - 0 1")["board"]
    assert piece_terms(half_open) == ROOK_HALF_OPEN_FILE


def test_static_exchange() -> None:
    """Qxd5 defended by a knight loses 800; exd5 undefended wins 100; Rxd5 with a
    rook behind it against one defender wins the pawn and trades: 100."""
    board = state_from_fen("4k3/8/5n2/3p4/8/8/8/3QK3 w - - 0 1")["board"]
    assert static_exchange(board, Move((7, 3), (3, 3))) == -800
    board = state_from_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")["board"]
    assert static_exchange(board, Move((4, 4), (3, 3))) == 100
    board = state_from_fen("3rk3/8/8/3p4/8/8/3R4/3RK3 w - - 0 1")["board"]
    assert static_exchange(board, Move((6, 3), (3, 3))) == 100


def test_quiescence_skips_a_losing_capture() -> None:
    """Qxd5 loses the queen, so quiescence stands pat with the static score."""
    state = state_from_fen("4k3/8/5n2/3p4/8/8/8/3QK3 w - - 0 1")
    before = state_snapshot(state)
    info = SearchInfo()
    quiescence(state, *WIDE, info)
    assert info.nodes == 1
    assert state_snapshot(state) == before


def test_futility_pruning_keeps_the_answer() -> None:
    """A rook down at depth 2: futility prunes quiet moves, but the root is unchanged."""
    state = state_from_fen("r3k3/8/8/8/8/8/PPP5/1K6 w - - 0 1")
    before = state_snapshot(state)
    score, _ = upgraded_search(state, 2, 1, -50, 50, SearchInfo())
    assert score <= -50
    assert state_snapshot(state) == before


def test_aspiration_matches_the_full_window() -> None:
    """Expected: the same score with a guess far off (a re-search) and with no guess."""
    state = state_from_fen("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1")
    score, pv = aspiration_search(state, 2, 400, SearchInfo())
    full, _ = aspiration_search(state, 2, None, SearchInfo())
    assert score == full == MATE_SCORE - 1
    assert move_to_uci(pv[0]) == "a1a8"


def test_think_stops_early_on_a_stable_move() -> None:
    """A stable best move ends the search well before a long hard limit."""
    state = state_from_fen("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    start = time.perf_counter()
    think(state, 0.5, max_seconds=5.0)
    assert time.perf_counter() - start < 3.0


def test_longest_time_is_a_multiple_of_the_plan() -> None:
    """63 seconds left: plan (63 - 3) / 30 = 2 seconds, longest 6 seconds."""
    words = ["go", "wtime", "63000", "btime", "63000"]
    assert thinking_time(words, True) == 2.0
    assert longest_time(words, True) == 6.0
    assert longest_time(["go", "movetime", "1500"], True) == 1.5
