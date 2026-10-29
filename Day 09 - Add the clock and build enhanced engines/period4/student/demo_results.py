#!/usr/bin/env -S uv run
"""demo_results.py

Day 9, period 4 demo: read a battle result. Part 1 turns wins, draws, and losses
into an Elo gap, and Part 2 adds a 95 percent margin, the way the class reads its
battles and the teacher's league.
Replace each line that holds only # with one line of code, then run the file.
"""

import math


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
    # Put your own battle result here, or your color's league games
    wins, draws, losses = 9, 4, 7
    #
    #
    #
    #
    #
    print("  (expected 11.0 points of 20: score 0.55, Elo gap +35)")

    print("Part #2 - The Margin of Error")
    # 95 percent of the time the true score lies within about 2 standard errors
    #
    #
    #
    #
    print("  (expected between -121 and +208)")
    # A gap is real when its whole range sits on one side of 0
    #
        #
    #
        #


if __name__ == "__main__":
    main()
