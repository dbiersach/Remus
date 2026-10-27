"""test_search.py

Tests for evaluation, minimax, and negamax.
"""

from evaluation import evaluate, material, placement
from fen import START_FEN, state_from_fen

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
