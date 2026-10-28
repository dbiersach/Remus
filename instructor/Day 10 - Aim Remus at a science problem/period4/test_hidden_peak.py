"""test_hidden_peak.py

Tests for the hidden-peak Science AI: the grid, the greedy agent, and the benchmark
against random guessing.
"""

from hidden_peak import (
    PEAK,
    benchmark,
    candidate_squares,
    choose_next_measurement,
    make_grid,
    random_strategy,
)


def test_hidden_peak_grid_has_one_peak() -> None:
    grid = make_grid(7)
    assert sum(row.count(PEAK) for row in grid) == 1
    assert make_grid(7) == grid  # The same seed makes the same sample


def test_greedy_ai_measures_where_it_looks_hot() -> None:
    readings = {(5, 5): 10, (2, 2): 90}
    choice = choose_next_measurement(readings, explore_weight=0)
    assert choice in candidate_squares(readings)
    assert abs(choice[0] - 2) <= 1 and abs(choice[1] - 2) <= 1


def test_greedy_ai_beats_random_guessing() -> None:
    """Over 20 samples random guessing needs far more measurements than greedy."""
    assert benchmark(choose_next_measurement, 20) < benchmark(random_strategy, 20) / 2
