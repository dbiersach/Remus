"""test_beam_time.py

Tests for the beam time agent: the estimate, the evaluation, the look-ahead, and
the benchmark against random and equal-time agents.
"""

import math

from beam_time import (
    SAMPLES,
    SHOTS,
    THRESHOLD,
    benchmark,
    chance_wrong,
    choose_next_sample,
    equal_time,
    estimate,
    expected_wrong_calls,
    gain,
    make_samples,
    run_experiment,
)


def test_four_readings_halve_the_error() -> None:
    average, error = estimate([48.0, 52.0, 47.0, 53.0], 10.0)
    assert average == 50.0
    assert error == 5.0


def test_a_call_at_the_threshold_is_a_coin_flip() -> None:
    assert chance_wrong(THRESHOLD, 10.0) == 0.5
    assert chance_wrong(THRESHOLD + 30.0, 10.0) < 0.01  # Three errors away


def test_unmeasured_samples_count_as_coin_flips() -> None:
    readings = [[] for _ in range(SAMPLES)]
    assert expected_wrong_calls(readings, [10.0] * SAMPLES) == SAMPLES * 0.5
    readings[0] = [90.0]
    assert math.isclose(
        expected_wrong_calls(readings, [10.0] * SAMPLES),
        (SAMPLES - 1) * 0.5,
        abs_tol=1e-4,
    )


def test_gain_favors_a_close_call_over_a_safe_one() -> None:
    assert gain([], 10.0) == 1.0  # Measure every sample once first
    assert gain([52.0], 10.0) > gain([90.0], 10.0)


def test_the_agent_measures_every_sample_once_first() -> None:
    samples = make_samples(1)
    noises = [sample["noise"] for sample in samples]
    readings = run_experiment(samples, choose_next_sample, seed=1)
    assert sum(len(sample_readings) for sample_readings in readings) == SHOTS
    assert all(readings)
    assert choose_next_sample([[]] * SAMPLES, noises) == 0


def test_largest_gain_beats_equal_time() -> None:
    _, smart_wrong = benchmark(choose_next_sample, trials=100)
    _, equal_wrong = benchmark(equal_time, trials=100)
    assert smart_wrong < equal_wrong
