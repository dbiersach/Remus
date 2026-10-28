#!/usr/bin/env -S uv run
"""compare_search.py

Compare negamax with alpha-beta on ten positions. Both must find the same score;
alpha-beta must visit fewer positions to get it.
"""

from fen import state_from_fen
from search import MATE_SCORE, SearchInfo, alpha_beta, negamax

POSITIONS = [  # Ten positions from the opening, middlegame, and endgame
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
DEPTH = 3  # Deep enough for pruning to matter, quick enough for plain negamax


def main():
    total_plain = 0
    total_pruned = 0
    for number, fen in enumerate(POSITIONS, start=1):
        state = state_from_fen(fen)
        plain = SearchInfo()
        plain_score = negamax(state, DEPTH, 0, plain)
        pruned = SearchInfo()
        pruned_score = alpha_beta(
            state, DEPTH, 0, -MATE_SCORE - 1, MATE_SCORE + 1, pruned
        )
        same = "same score" if plain_score == pruned_score else "DIFFERENT SCORE"
        print(
            f"{number:2}. negamax {plain.nodes:7,} positions, alpha-beta {pruned.nodes:6,}"
            f" positions, {same}"
        )
        total_plain += plain.nodes
        total_pruned += pruned.nodes
    print(
        f"Alpha-beta visited {total_pruned / total_plain:.0%} of the positions negamax"
        " visited  (expected well under 50%)"
    )


if __name__ == "__main__":
    main()
