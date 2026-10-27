"""test_beam_time.py

Tests for the beam time agent: the estimate, the evaluation, and the random and
equal-time agents.
"""

import math

from beam_time import (
    SAMPLES,
    THRESHOLD,
    chance_wrong,
    estimate,
    expected_wrong_calls,
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
