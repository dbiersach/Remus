#!/usr/bin/env -S uv run
"""hidden_peak.py

Science AI: aim the engine's loop of "list the candidates, score each one, choose
the best" at a measurement problem.

A 10x10 sample hides a hot spot. Each measurement reads the value at one square,
from 0 far away up to 100 at the peak. The goal is to find the peak in as few
measurements as possible, the same choice an AI agent makes at a beamline at
Brookhaven's NSLS-II: where to measure next.

| Chess engine | Hidden peak |
| --- | --- |
| Legal moves | Squares not yet measured |
| Evaluation | Predicted value (exploit) plus distance from earlier readings (explore) |
| greedy_move() | Measure the best-scoring square now |
| Minimax: the opponent picks the minimum | Expectimax: average over a high or low reading |
| A match against greedy Remus | A benchmark: average measurements over 100 hidden samples |

This file uses the standard library only and does not import the engine: it reuses
the engine's ideas, not its code.
"""

import math
import random

SIZE = 10  # The sample is SIZE x SIZE squares
PEAK = 100  # The reading at the hot spot
EXPLORE_WEIGHT = 8  # Points of score per square of distance from the nearest reading


def make_grid(seed: int) -> list[list[int]]:
    """
    Make a hidden sample: a hot spot at a random square, fading with distance.

    Parameters
    ----------
    seed : int
        The random seed, so the same seed always makes the same sample.

    Returns
    -------
    list[list[int]]
        grid[row][col] holds the reading at that square, from 0 to PEAK.
    """
    chooser = random.Random(seed)
    peak_row = chooser.randrange(SIZE)
    peak_col = chooser.randrange(SIZE)
    width = chooser.uniform(1.0, 2.5)  # How far the heat spreads
    grid = []
    for row in range(SIZE):
        values = []
        for col in range(SIZE):
            distance = math.dist((row, col), (peak_row, peak_col))
            values.append(round(PEAK * math.exp(-((distance / width) ** 2))))
        grid.append(values)
    return grid


def measure(grid: list[list[int]], square: tuple[int, int]) -> int:
    """Return the reading at one square of the hidden sample."""
    row, col = square
    return grid[row][col]


def predicted_value(
    square: tuple[int, int], readings: dict[tuple[int, int], int]
) -> float:
    """
    Predict the reading at a square from the readings so far.

    Each reading counts more the closer it is (an inverse-distance average), so a
    square next to a hot reading is predicted to be hot.
    """
    total = 0.0
    weights = 0.0
    for measured, value in readings.items():
        distance = math.dist(square, measured)
        weight = 1 / distance**2
        total += weight * value
        weights += weight
    return total / weights


def candidate_squares(readings: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    """
    Return every square not yet measured, the "legal moves" of this problem.

    Parameters
    ----------
    readings : dict[tuple[int, int], int]
        The readings so far, keyed by (row, col).

    Returns
    -------
    list[tuple[int, int]]
        The unmeasured squares, row by row.
    """
    squares = []
    for row in range(SIZE):
        for col in range(SIZE):
            if (row, col) not in readings:
                squares.append((row, col))
    return squares


def score_candidate(
    square: tuple[int, int], readings: dict[tuple[int, int], int], explore_weight: float
) -> float:
    """
    Score a square as the next measurement, the "evaluation" of this problem.

    Parameters
    ----------
    square : tuple[int, int]
        The square to score.
    readings : dict[tuple[int, int], int]
        The readings so far.
    explore_weight : float
        How much to value distance from earlier readings. 0 means "only measure
        where it already looks hot"; a large value means "spread out and look
        everywhere".

    Returns
    -------
    float
        The predicted value (exploit) plus explore_weight times the distance to the
        nearest reading (explore).
    """
    nearest = min(math.dist(square, measured) for measured in readings)
    return predicted_value(square, readings) + explore_weight * nearest


def choose_next_measurement(
    readings: dict[tuple[int, int], int], explore_weight: float = EXPLORE_WEIGHT
) -> tuple[int, int]:
    """Return the unmeasured square with the highest score, like greedy_move()."""
    return max(
        candidate_squares(readings),
        key=lambda square: score_candidate(square, readings, explore_weight),
    )


def random_strategy(readings: dict[tuple[int, int], int]) -> tuple[int, int]:
    """Measure a random unmeasured square, the baseline every AI must beat."""
    return random.choice(candidate_squares(readings))


def expectimax_choice(
    readings: dict[tuple[int, int], int], explore_weight: float = EXPLORE_WEIGHT
) -> tuple[int, int]:
    """
    Look two measurements ahead (teacher demo).

    For each candidate, imagine the reading coming back 20 points higher or 20
    points lower than predicted, each half the time. Value each outcome as the
    pretend reading plus the best score of the measurement after it, then average
    the two outcomes. Chess search takes the opponent's minimum here; nature is
    not an opponent, so this search averages. Averages give no cutoffs, which is
    why alpha-beta has nothing to prune.

    The benchmark shows this lookahead doing worse than the greedy AI: looking
    ahead only helps when the predictions are good, and a "plus or minus 20" guess
    is not. The NSLS-II agent uses a statistical model (a Gaussian process) that
    knows how uncertain each prediction is.
    """
    best_square = None
    best_value = -math.inf
    for square in candidate_squares(readings):
        guess = predicted_value(square, readings)
        outcomes = []
        for reading in (min(PEAK, guess + 20), max(0, guess - 20)):
            readings[square] = round(reading)  # Pretend to measure, like make_move
            next_best = max(
                (
                    score_candidate(other, readings, explore_weight)
                    for other in candidate_squares(readings)
                ),
                default=0,
            )
            del readings[square]  # Take the pretend reading back, like undo_move
            outcomes.append(reading + next_best)
        value = sum(outcomes) / len(outcomes)
        if value > best_value:
            best_square, best_value = square, value
    return best_square


def measurements_to_find_peak(grid: list[list[int]], strategy) -> int:
    """Run one strategy on one sample and count measurements until it reads PEAK."""
    center = (SIZE // 2, SIZE // 2)
    readings = {center: measure(grid, center)}  # Every strategy starts in the middle
    while PEAK not in readings.values():
        square = strategy(readings)
        readings[square] = measure(grid, square)
    return len(readings)


def benchmark(strategy, trials: int = 100) -> float:
    """
    Return the average number of measurements a strategy needs over many samples.

    Parameters
    ----------
    strategy : callable
        Takes the readings so far and returns the next square to measure.
    trials : int
        How many hidden samples to try. Sample n always uses seed n, so every
        strategy faces the same samples.

    Returns
    -------
    float
        The average measurements needed to find the peak.
    """
    random.seed(0)  # The random strategy makes the same choices every run
    total = 0
    for seed in range(trials):
        total += measurements_to_find_peak(make_grid(seed), strategy)
    return total / trials


def main():
    print(f"Random guessing: {benchmark(random_strategy):5.1f} measurements on average")
    for weight in (0, EXPLORE_WEIGHT, 40):
        average = benchmark(
            lambda readings, w=weight: choose_next_measurement(readings, w)
        )
        print(
            f"Greedy AI, explore weight {weight:2}: {average:5.1f} measurements on average"
        )
    print(
        "  (expected: every greedy AI well below random guessing, best near weight 8)"
    )
    average = benchmark(expectimax_choice, trials=10)
    print(f"Expectimax AI (10 samples): {average:5.1f} measurements on average")
    print(
        "  (expected: better than random, worse than greedy: a crude model limits lookahead)"
    )


if __name__ == "__main__":
    main()
