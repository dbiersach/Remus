"""test_phase_hunt.py

Tests for the phase hunt: the evaluation and the greedy agent.
"""

from phase_hunt import (
    LIBRARY,
    SILVER_POWDER,
    greedy_phases,
    make_pattern,
    matches,
    score,
)


def test_peaks_match_within_the_tolerance() -> None:
    assert matches(28.5, [20.9, 28.4])
    assert not matches(28.9, [20.9, 28.4])


def test_score_rewards_explained_peaks_and_punishes_the_rest() -> None:
    quartz = LIBRARY["quartz"]
    assert score([], quartz) == -4  # Four peaks left over
    assert score(["quartz"], quartz) == 3  # Four explained, one phase used
    # Rutile explains nothing here: four predicted peaks are missing
    assert score(["quartz", "rutile"], quartz) == -2


def test_greedy_names_a_clean_mixture() -> None:
    measured = sorted(LIBRARY["quartz"] + LIBRARY["rutile"])
    assert sorted(greedy_phases(measured)) == ["quartz", "rutile"]


def test_greedy_mistakes_silver_for_gold() -> None:
    measured, truth = make_pattern(SILVER_POWDER)
    assert truth == ["anatase", "silver"]
    assert sorted(greedy_phases(measured)) == ["anatase", "gold"]
