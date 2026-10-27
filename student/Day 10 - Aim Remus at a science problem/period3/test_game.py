"""test_game.py

Tests for FEN, SAN, the end of the game, and the UCI engine. python-chess is the
independent reference for FEN and SAN.
"""

import subprocess
import sys
from pathlib import Path

import chess
from fen import START_FEN, state_from_fen, state_to_fen
from game_end import game_result, insufficient_material
from game_state import new_game
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from moves import move_from_uci, move_to_uci
from notation import move_to_san, parse_san
from search import greedy_move

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


def test_san_matches_python_chess_for_every_legal_move() -> None:
    for fen in FENS:
        state = state_from_fen(fen)
        board = chess.Board(fen)
        for move in legal_moves(state):
            expected = board.san(chess.Move.from_uci(move_to_uci(move)))
            assert move_to_san(state, move) == expected, (fen, expected)


def test_parse_san_finds_each_move() -> None:
    state = state_from_fen(FENS[1])
    for move in legal_moves(state):
        assert parse_san(state, move_to_san(state, move)) == move


def test_checkmate_and_stalemate() -> None:
    mate = state_from_fen(
        "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
    )
    assert game_result(mate) == ("0-1", "checkmate")
    stalemate = state_from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert game_result(stalemate) == ("1/2-1/2", "stalemate")


def test_insufficient_material() -> None:
    assert insufficient_material(
        state_from_fen("8/8/4k3/8/8/2N5/8/4K3 w - - 0 1")["board"]
    )
    # Bishops on d6 and e3 both stand on dark squares; c6 is a light square
    assert insufficient_material(
        state_from_fen("8/8/3bk3/8/8/4B3/8/4K3 w - - 0 1")["board"]
    )
    assert not insufficient_material(
        state_from_fen("8/8/2b1k3/8/8/4B3/8/4K3 w - - 0 1")["board"]
    )
    assert not insufficient_material(
        state_from_fen("8/8/4k3/8/8/4P3/8/4K3 w - - 0 1")["board"]
    )


def test_threefold_repetition_and_undo() -> None:
    state = new_game()
    for _ in range(2):
        for text in ["g1f3", "g8f6", "f3g1", "f6g8"]:
            make_move(state, move_from_uci(text))
    assert game_result(state) == ("1/2-1/2", "threefold repetition")
    undo = make_move(state, move_from_uci("e2e4"))
    undo_move(state, undo)
    assert len(state["history"]) == 9


def test_fifty_move_rule() -> None:
    outcome = game_result(state_from_fen("8/8/4k3/8/8/4R3/8/4K3 w - - 100 80"))
    assert outcome is not None
    assert outcome[1] == "fifty-move rule"


def test_greedy_takes_the_queen() -> None:
    state = state_from_fen("4k3/8/8/3q4/8/2N1p3/8/4K3 w - - 0 1")
    assert move_to_uci(greedy_move(state)) == "c3d5"


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
