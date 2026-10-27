"""test_upgrades.py

Tests for the RED station: the transposition table and table_search.
"""

from fen import START_FEN, state_from_fen
from game_state import position_key
from make_move import make_move, state_snapshot
from moves import Move, move_from_uci
from search import MATE_SCORE, SearchInfo, alpha_beta_with_quiescence, table_search
from transposition_table import EXACT, LOWER, UPPER, best_stored_move, probe, store

ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside


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


def test_table_search_agrees_with_alpha_beta() -> None:
    """The station saves work but finds the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = table_search(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before
