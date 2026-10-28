#!/usr/bin/env -S uv run
"""remus_benchmark.py

Time one Remus version on the ten positions of compare_search.py, so its speed can
be compared with the Niram engine of the same color, the Rust copy of that version.
Each position gets that version's own think(), one depth at a time up to the depth
asked for, with no clock, so both engines visit exactly the same positions.

Run it from the repository folder:

    uv run scripts/remus_benchmark.py GOLD        Remus-GOLD, depth 4
    uv run scripts/remus_benchmark.py WHITE 5     Remus-WHITE, depth 5

and the matching Rust benchmark from inside Niram/:

    cargo run --release -p niram-gold -- bench
    cargo run --release -p niram-white -- bench 5
"""

import sys
import time
from pathlib import Path

STATIONS = Path(__file__).parent.parent / "instructor" / "Remus"
DEPTH = 4  # The deepest iteration, the same for both engines
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
MATE_SCORE = 100_000  # The same as search.py


def find_folder(color: str) -> Path:
    """Return the station folder of a color: "RED" finds "06 RED - Transposition table"."""
    for folder in sorted(STATIONS.iterdir()):
        if folder.is_dir() and " - " in folder.name:
            words = folder.name.split(" - ")[0].split()
            if words[len(words) - 1] == color.upper():
                return folder
    sys.exit(f"No station folder has the color {color!r}")


def score_from_info(line: str) -> int:
    """Return the score of an info line ("cp 35" gives 35, "mate 1" gives 99999)."""
    words = line.split()
    index = words.index("score")
    value = int(words[index + 2])
    if words[index + 1] == "mate":
        plies = 2 * abs(value) - 1
        return MATE_SCORE - plies if value > 0 else -(MATE_SCORE - plies)
    return value


def main():
    color = sys.argv[1] if len(sys.argv) > 1 else "GOLD"
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else DEPTH
    folder = find_folder(color)
    sys.path.insert(0, str(folder))  # Import that version's own modules

    import search
    from fen import state_from_fen
    from moves import move_to_uci

    # think() makes its own SearchInfo, so a SearchInfo that remembers itself lets
    # the benchmark read the positions think() visited
    searches = []

    class RecordingInfo(search.SearchInfo):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            searches.append(self)

    search.SearchInfo = RecordingInfo
    name = "Remus-" + folder.name.split(" - ")[0]
    print(f"{name} (Python), iterative deepening to depth {max_depth}")
    total_nodes = 0
    total_seconds = 0.0
    for number, fen in enumerate(POSITIONS, start=1):
        state = state_from_fen(fen)
        lines = []
        start = time.perf_counter()
        best = search.think(state, 1_000_000.0, max_depth, report=lines.append)
        seconds = time.perf_counter() - start
        nodes = searches[-1].nodes
        score = score_from_info(lines[-1])
        total_nodes += nodes
        total_seconds += seconds
        print(
            f"{number:2}. {move_to_uci(best):6} score {score:7}  nodes {nodes:10,}"
            f"  {seconds:8.3f} s  {nodes / seconds:12,.0f} nodes/s"
        )
    print(f"Total nodes: {total_nodes:,}")
    print(f"Total run time (sec): {total_seconds:.3f}")
    print(f"Nodes per second: {total_nodes / total_seconds:,.0f}")


if __name__ == "__main__":
    main()
