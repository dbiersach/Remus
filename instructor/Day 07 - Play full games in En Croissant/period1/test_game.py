"""test_game.py

Tests for FEN, SAN, the end of the game, and the UCI engine. python-chess is the
independent reference for FEN and SAN.
"""

import subprocess
import sys
from pathlib import Path

import chess
from fen import START_FEN, state_from_fen, state_to_fen
from game_state import new_game
from make_move import state_snapshot

FENS = [  # Positions with every kind of move: castling, en passant, promotion, checks
    START_FEN,
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3",
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "1k6/3P4/8/8/8/8/8/R2K1R2 w - - 0 1",
]


def test_fen_round_trip() -> None:
    for fen in FENS:
        assert state_to_fen(state_from_fen(fen)) == fen


def test_new_game_matches_start_fen() -> None:
    assert state_snapshot(new_game()) == state_snapshot(state_from_fen(START_FEN))


def test_uci_engine_answers_the_gui() -> None:
    engine = Path(__file__).parent / "uci_engine.py"
    commands = "uci\nisready\nposition startpos moves e2e4 e7e5\ngo\nquit\n"
    output = subprocess.run(
        [sys.executable, str(engine)],
        input=commands,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    ).stdout
    lines = output.split("\n")
    assert "uciok" in lines and "readyok" in lines
    best = next(line for line in lines if line.startswith("bestmove")).split()[1]
    board = chess.Board()
    board.push_uci("e2e4")
    board.push_uci("e7e5")
    assert chess.Move.from_uci(best) in board.legal_moves
