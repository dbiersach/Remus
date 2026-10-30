#!/usr/bin/env -S uv run
"""perft.py

Count the leaf positions of the legal move tree to a fixed depth ("perft", for
performance test). Chess programmers have published these counts for many
positions, so a matching count is strong evidence that every rule is right.
"""

import time

from game_state import new_game
from legal_moves import legal_moves
from make_move import make_move, undo_move
from moves import move_to_uci

START_COUNTS = [
    1,
    20,
    400,
    8_902,
    197_281,
]  # Published counts from the start, depth 0 to 4


def perft(state: dict, depth: int) -> int:
    """
    Count the positions reached after exactly `depth` moves.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when perft returns.
    depth : int
        The number of moves (plies) to look ahead.

    Returns
    -------
    int
        The number of leaf positions. At depth 0 the position itself counts as 1.
    """
    if depth == 0:
        return 1
    count = 0
    for move in legal_moves(state):
        undo = make_move(state, move)
        count += perft(state, depth - 1)  # Recursive call to itself
        undo_move(state, undo)
    return count


def divide(state: dict, depth: int) -> dict[str, int]:
    """
    Split a perft count by root move, to find which move a bug hides under.

    Parameters
    ----------
    state : dict
        The game state.
    depth : int
        The perft depth, counting the root move.

    Returns
    -------
    dict[str, int]
        The count under each root move, keyed by its UCI text.
    """
    counts = {}
    for move in legal_moves(state):
        undo = make_move(state, move)
        counts[move_to_uci(move)] = perft(state, depth - 1)
        undo_move(state, undo)
    return counts


def main():
    state = new_game()
    for depth in range(1, 4):
        start = time.perf_counter()
        count = perft(state, depth)
        seconds = time.perf_counter() - start
        print(
            f"perft({depth}) = {count:,}  (expected {START_COUNTS[depth]:,})  {seconds:.2f} s"
        )
    print(f"divide(2) under e2e4: {divide(state, 2)['e2e4']}  (expected 20)")


if __name__ == "__main__":
    main()
