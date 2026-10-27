#!/usr/bin/env -S uv run
"""hunt.py

Day 6, period 3 demo: the bug hunt. The Remus files in this bug_hunt folder are a
copy of the period's code with three bugs planted in them. This script runs
divide() on four standard positions and prints every root move where Remus and
python-chess count a different number of positions. Each such move points at a
bug: find it in the code, fix it, and run the hunt again until every count agrees.
"""

import chess
from board import EMPTY
from game_state import BLACK, WHITE, new_game
from perft import divide

DEPTH = 2  # Two moves deep: each root move and every reply to it
POSITIONS = [  # (name, FEN): standard perft positions from the Chess Programming Wiki
    (
        "kiwipete",
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    ),
    ("position 3", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"),
    ("position 4", "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"),
    ("position 5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"),
]


def state_from_python_chess(board: chess.Board) -> dict:
    """Build a Remus state from a python-chess board, because Remus reads FEN in period 4."""
    state = new_game()
    state["board"] = [[EMPTY] * 8 for _ in range(8)]
    for square, piece in board.piece_map().items():
        # python-chess counts rank 1 as 0, and Remus puts rank 8 on row 0
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        state["board"][row][col] = piece.symbol()
    state["turn"] = WHITE if board.turn == chess.WHITE else BLACK
    state["castling"] = board.castling_xfen().replace("-", "")
    state["en_passant"] = None
    if board.ep_square is not None:
        row = 7 - chess.square_rank(board.ep_square)
        state["en_passant"] = (row, chess.square_file(board.ep_square))
    return state


def reference_count(board: chess.Board, depth: int) -> int:
    """Count the positions after `depth` moves with python-chess, the reference."""
    if depth == 0:
        return 1
    count = 0
    for move in list(board.legal_moves):
        board.push(move)
        count += reference_count(board, depth - 1)
        board.pop()
    return count


def main():
    wrong_moves = 0
    for name, fen in POSITIONS:
        board = chess.Board(fen)
        remus_counts = divide(state_from_python_chess(board), DEPTH)
        print(
            f"{name}: {len(remus_counts)} root moves in Remus, {board.legal_moves.count()} in python-chess"
        )
        for move in board.legal_moves:
            board.push(move)
            expected = reference_count(board, DEPTH - 1)
            board.pop()
            found = remus_counts.get(move.uci(), 0)
            if found != expected:
                print(
                    f"  under {move.uci()}: Remus counts {found}, python-chess {expected}"
                )
                wrong_moves += 1
    print(
        f"Root moves that disagree: {wrong_moves}  (expected 0 once every bug is fixed)"
    )


if __name__ == "__main__":
    main()
