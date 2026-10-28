"""test_search.py

Tests for evaluation, minimax, and negamax.
"""

from pathlib import Path

from evaluation import evaluate, material, placement
from fen import START_FEN, state_from_fen
from make_move import state_snapshot
from moves import move_to_uci
from search import (
    MATE_SCORE,
    SearchInfo,
    alpha_beta,
    best_move,
    minimax,
    negamax,
    quiescence,
)

MATE_PUZZLES = (
    Path(__file__).parent / "mate_puzzles.epd"
)  # Ten puzzles, MATE.001 to MATE.010

MATES_IN_ONE = [  # (FEN, the mating move)
    ("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1", "a1a8"),  # Back-rank mate
    (
        "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
        "d8h4",
    ),  # Fool's mate
    ("k7/8/1K6/8/8/8/7Q/8 w - - 0 1", "h2h8"),  # Queen and king
]


def test_start_position_is_level() -> None:
    state = state_from_fen(START_FEN)
    assert material(state["board"]) == 0
    assert placement(state["board"]) == 0


def test_evaluation_is_from_the_side_to_move() -> None:
    white = state_from_fen("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    black = state_from_fen("4k3/8/8/8/8/8/8/3QK3 b - - 0 1")
    assert evaluate(white) > 0
    assert evaluate(black) == -evaluate(white)


def test_mirrored_positions_score_the_same_for_the_mover() -> None:
    white = state_from_fen("4k3/8/8/8/3N4/8/8/4K3 w - - 0 1")
    black = state_from_fen("4k3/8/8/3n4/8/8/8/4K3 b - - 0 1")
    assert evaluate(white) == evaluate(black)


def test_negamax_finds_mate_in_one() -> None:
    for fen, expected in MATES_IN_ONE:
        move, score, _ = best_move(state_from_fen(fen), 2)
        assert move_to_uci(move) == expected
        assert score == MATE_SCORE - 1
        assert negamax(state_from_fen(fen), 2, 0, SearchInfo()) == MATE_SCORE - 1


def test_minimax_and_negamax_agree() -> None:
    for fen in [
        START_FEN,
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    ]:
        state = state_from_fen(fen)
        white_view = minimax(state, 2, SearchInfo())
        mover_view = negamax(state, 2, 0, SearchInfo())
        assert white_view == mover_view  # White is to move in both positions


def test_stalemate_scores_zero() -> None:
    state = state_from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert negamax(state, 2, 0, SearchInfo()) == 0


def test_search_leaves_the_root_unchanged() -> None:
    state = state_from_fen(
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    )
    before = state_snapshot(state)
    best_move(state, 2)
    assert state_snapshot(state) == before


def test_greedy_trap_is_avoided() -> None:
    """The pawn on d5 is defended by the e6 pawn; looking ahead, the queen keeps away."""
    state = state_from_fen("4k3/8/4p3/3p4/8/8/3Q4/4K3 w - - 0 1")
    move, _, _ = best_move(state, 2)
    assert move_to_uci(move) != "d2d5"


def test_alpha_beta_matches_negamax_with_fewer_positions() -> None:
    for fen in [
        START_FEN,
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    ]:
        state = state_from_fen(fen)
        plain, pruned = SearchInfo(), SearchInfo()
        expected = negamax(state, 3, 0, plain)
        assert (
            alpha_beta(state, 3, 0, -MATE_SCORE - 1, MATE_SCORE + 1, pruned) == expected
        )
        assert pruned.nodes < plain.nodes


def test_quiescence_stands_pat_or_takes_a_free_pawn() -> None:
    """Expected: a defended pawn is left alone, a free pawn is taken."""
    defended = state_from_fen("4k3/8/4p3/3p4/8/8/3Q4/4K3 w - - 0 1")
    before = state_snapshot(defended)
    score = quiescence(defended, -MATE_SCORE - 1, MATE_SCORE + 1, SearchInfo())
    assert score == evaluate(defended)  # Qxd5 exd5 loses the queen, so stand pat
    assert state_snapshot(defended) == before
    free = state_from_fen("4k3/8/8/3p4/8/8/3Q4/4K3 w - - 0 1")
    score = quiescence(free, -MATE_SCORE - 1, MATE_SCORE + 1, SearchInfo())
    assert score > evaluate(free)  # Qxd5 wins a pawn that nothing defends
