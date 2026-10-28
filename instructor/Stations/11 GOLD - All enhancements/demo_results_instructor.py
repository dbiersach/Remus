#!/usr/bin/env -S uv run
"""demo_results_instructor.py

Day 10, period 4 demo: read a match result and explain one move. Part 1 turns
wins, draws, and losses into an Elo gap with a 95 percent margin, the way the
class reads its station matches. Part 2 asks Remus to think about one position
and prints its score and principal variation at every depth.
The student file demo_results.py leaves one # line for each line the pair types.
"""

import math

from fen import state_from_fen
from moves import move_to_uci
from search import think


def elo_gap(score: float) -> float:
    """
    Return the rating gap that the Elo formula expects for a score.

    Parameters
    ----------
    score : float
        Points per game, from 0 (lost every game) to 1 (won every game).

    Returns
    -------
    float
        The rating gap in Elo points: 0 for a score of 0.5, positive above it.
    """
    # A score of exactly 0 or 1 fits any gap, so keep the score just inside
    score = min(max(score, 0.01), 0.99)
    return -400 * math.log10(1 / score - 1)


def main():
    print("Part #1 - Points, Score, and Elo Gap")
    # Put your own color's result against Remus-WHITE here
    wins, draws, losses = 9, 4, 7
    games = wins + draws + losses
    points = wins + draws / 2
    score = points / games
    gap = elo_gap(score)
    print(f"{points} points of {games}: score {score:.2f}, Elo gap {gap:+.0f}")
    print("  (expected 11.0 points of 20: score 0.55, Elo gap +35)")

    print("Part #2 - The Margin of Error")
    # 95 percent of the time the true score lies within about 2 standard errors
    margin = 1.96 * math.sqrt(score * (1 - score) / games)
    low = elo_gap(score - margin)
    high = elo_gap(score + margin)
    print(f"The Elo gap lies between {low:+.0f} and {high:+.0f}")
    print("  (expected between -121 and +208)")
    # A gap is real when its whole range sits on one side of 0
    if low > 0 or high < 0:
        print("The gap is larger than its margin: the enhancement made a difference")
    else:
        print("The margin reaches past 0: more games are needed to be sure")

    print("Part #3 - Explain One Move")
    # A back-rank mate: White's rook reaches a8 and Black's own pawns trap the king
    state = state_from_fen("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1")
    # report=print shows the depth, score, nodes, and principal variation of each search
    move = think(state, seconds=2.0, report=print)
    print(f"Remus plays {move_to_uci(move)}  (expected a1a8, score mate 1)")


if __name__ == "__main__":
    main()
