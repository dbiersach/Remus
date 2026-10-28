"""test_phase_hunt.py

Tests for the phase hunt: the evaluation, the greedy agent, the tree search, and the
benchmark against known powders.
"""

from phase_hunt import (
    LIBRARY,
    MAX_PHASES,
    SILVER_POWDER,
    Hunt,
    benchmark,
    greedy_answer,
    greedy_phases,
    make_pattern,
    matches,
    run_search,
    score,
    search,
    search_answer,
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


def test_search_leaves_the_phases_as_it_found_them() -> None:
    measured = sorted(LIBRARY["quartz"] + LIBRARY["rutile"])
    phases = ["quartz"]
    hunt = Hunt(score=score(phases, measured))
    search(phases, measured, 2, 3, hunt)
    assert phases == ["quartz"]


def test_search_scores_each_set_once() -> None:
    measured, _ = make_pattern(0)
    # 1 empty set + 10 sets of one + 45 sets of two + 120 sets of three
    assert run_search(measured).nodes == 176


def test_search_finds_both_look_alikes() -> None:
    measured, _ = make_pattern(SILVER_POWDER)
    hunt = run_search(measured)
    assert hunt.sets == [["anatase", "gold"], ["anatase", "silver"]]
    for phases in hunt.sets:
        assert len(phases) <= MAX_PHASES


def test_search_makes_fewer_wrong_calls_than_greedy() -> None:
    greedy = benchmark(greedy_answer, trials=100)
    searched = benchmark(search_answer, trials=100)
    assert searched["wrong"] < greedy["wrong"]
