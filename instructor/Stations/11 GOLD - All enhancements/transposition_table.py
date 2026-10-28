#!/usr/bin/env -S uv run
"""transposition_table.py

Remember positions the search has already scored. The same position can arise in
many orders (1. Nf3 Nf6 2. Nc3 and 1. Nc3 Nf6 2. Nf3), so a plain dictionary keyed
by position_key saves the search from scoring it twice.

Each entry stores the depth searched, the score, the kind of score, and the best
move. An alpha-beta score is not always exact:

- "exact": the true score at that depth.
- "lower": a cutoff happened, so the true score is at least this much.
- "upper": no move beat alpha, so the true score is at most this much.
"""

from fen import START_FEN, state_from_fen
from game_state import position_key
from moves import Move

EXACT = "exact"  # The score is exact
LOWER = "lower"  # The true score is at least the stored score
UPPER = "upper"  # The true score is at most the stored score


def store(
    table: dict, key: str, depth: int, score: int, bound: str, best: Move | None
) -> None:
    """Save a search result for a position, keeping the deeper of two results."""
    old = table.get(key)
    if old is None or depth >= old["depth"]:
        table[key] = {"depth": depth, "score": score, "bound": bound, "best": best}


def probe(table: dict, key: str, depth: int, alpha: int, beta: int) -> int | None:
    """
    Return a stored score that answers this search, or None.

    Parameters
    ----------
    table : dict
        The transposition table.
    key : str
        The position_key of the position.
    depth : int
        The depth the search needs.
    alpha, beta : int
        The search window.

    Returns
    -------
    int | None
        The stored score if it was searched at least as deep and its bound settles
        the question: an exact score, a lower bound at or above beta (a cutoff),
        or an upper bound at or below alpha (no improvement). Otherwise None.
    """
    entry = table.get(key)
    if entry is None or entry["depth"] < depth:
        return None
    score = entry["score"]
    if entry["bound"] == EXACT:
        return score
    if entry["bound"] == LOWER and score >= beta:
        return score
    if entry["bound"] == UPPER and score <= alpha:
        return score
    return None


def best_stored_move(table: dict, key: str) -> Move | None:
    """Return the best move stored for a position, to try first."""
    entry = table.get(key)
    return None if entry is None else entry["best"]


def main():
    table = {}
    key = position_key(state_from_fen(START_FEN))
    store(table, key, 3, 25, EXACT, None)
    print(f"Probe at depth 3: {probe(table, key, 3, -100, 100)}  (expected 25)")
    print(
        f"Probe at depth 4: {probe(table, key, 4, -100, 100)}  (expected None: too shallow)"
    )


if __name__ == "__main__":
    main()
