"""test_perft.py

Compare Remus's perft counts with python-chess, an independent move generator, on
the standard test positions. From Day 7 on, Remus reads each FEN itself.
"""

import chess
from fen import state_from_fen
from game_state import new_game
from perft import START_COUNTS, divide, perft

POSITIONS = [  # (name, FEN, depth): standard perft positions from the Chess Programming Wiki
    ("start", chess.STARTING_FEN, 3),
    (
        "kiwipete",
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
        2,
    ),
    ("position 3", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 3),
    (
        "position 4",
        "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
        2,
    ),
    ("position 5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", 2),
]


def python_chess_perft(board: chess.Board, depth: int) -> int:
    if depth == 0:
        return 1
    count = 0
    for move in list(board.legal_moves):
        board.push(move)
        count += python_chess_perft(board, depth - 1)
        board.pop()
    return count


def test_start_position_counts() -> None:
    state = new_game()
    for depth in range(4):
        assert perft(state, depth) == START_COUNTS[depth]


def test_standard_positions_match_python_chess() -> None:
    for name, fen, depth in POSITIONS:
        board = chess.Board(fen)
        expected = python_chess_perft(board, depth)
        assert perft(state_from_fen(fen), depth) == expected, name


def test_divide_matches_python_chess_move_by_move() -> None:
    board = chess.Board(POSITIONS[1][1])
    counts = divide(state_from_fen(POSITIONS[1][1]), 2)
    for move in board.legal_moves:
        board.push(move)
        assert counts[move.uci()] == board.legal_moves.count(), move.uci()
        board.pop()
