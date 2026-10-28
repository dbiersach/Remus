#!/usr/bin/env -S uv run
"""remus_benchmark.py

Time Remus-GOLD on the ten positions of compare_search.py, so its speed can be
compared with Niram-GOLD, the Rust copy of the same engine. Each position gets the
same search that Remus-GOLD's think() runs, one depth at a time up to DEPTH, with
no clock, so both engines visit exactly the same positions.

Run it from the repository folder with `uv run niram/remus_benchmark.py`, and run
Niram-GOLD's benchmark with `cargo run --release -- bench` from inside niram/.
"""

import sys
import time
from pathlib import Path

GOLD_FOLDER = (
    Path(__file__).parent.parent / "instructor" / "Stations" / "11 GOLD - All enhancements"
)
sys.path.insert(0, str(GOLD_FOLDER))  # Import Remus-GOLD's own modules

from fen import state_from_fen
from legal_moves import legal_moves
from moves import move_to_uci
from search import MATE_SCORE, SearchInfo, upgraded_search

POSITIONS = [  # The ten positions of compare_search.py
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    "rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5",
    "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2PP1N2/PP3PPP/RNBQ1RK1 w - - 0 7",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "2r3k1/pp3ppp/8/3p4/3P4/8/PP3PPP/2R3K1 w - - 0 1",
    "8/5k2/8/3K4/8/8/4P3/8 w - - 0 1",
    "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",
    "4k3/8/4p3/3p4/8/8/3Q4/4K3 w - - 0 1",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
]
DEPTH = 4  # The deepest iteration, the same for both engines


def deepen(fen: str, max_depth: int) -> tuple[int, int, str]:
    """
    Search one position the way think() does, one depth at a time, with no clock.

    Parameters
    ----------
    fen : str
        The position.
    max_depth : int
        The deepest iteration.

    Returns
    -------
    tuple[int, int, str]
        The positions visited, the last score, and the best move in UCI text.
    """
    state = state_from_fen(fen)
    info = SearchInfo()
    moves = legal_moves(state)
    score = 0
    best = ""
    for depth in range(1, max_depth + 1):
        score, pv = upgraded_search(
            state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, info
        )
        if pv:
            best = move_to_uci(pv[0])
        if abs(score) > MATE_SCORE - 1000 or len(moves) == 1:
            break  # think() stops here too
    return info.nodes, score, best


def main():
    max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else DEPTH
    print(f"Remus-GOLD (Python), iterative deepening to depth {max_depth}")
    total_nodes = 0
    total_seconds = 0.0
    for number, fen in enumerate(POSITIONS, start=1):
        start = time.perf_counter()
        nodes, score, best = deepen(fen, max_depth)
        seconds = time.perf_counter() - start
        total_nodes += nodes
        total_seconds += seconds
        print(
            f"{number:2}. {best:6} score {score:7}  nodes {nodes:10,}"
            f"  {seconds:8.3f} s  {nodes / seconds:12,.0f} nodes/s"
        )
    print(f"Total nodes: {total_nodes:,}")
    print(f"Total run time (sec): {total_seconds:.3f}")
    print(f"Nodes per second: {total_nodes / total_seconds:,.0f}")


if __name__ == "__main__":
    main()
