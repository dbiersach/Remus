#!/usr/bin/env -S uv run
"""phase_hunt.py

Science AI: name the crystals in a powder from its X-ray pattern, with the same
tree search that chooses a chess move.

A beamline such as the PDF beamline at Brookhaven's NSLS-II shines X-rays through a
powder. The detector records peaks, each at an angle called 2-theta. Every crystal
phase (silicon, quartz, rutile, ...) makes its own fingerprint of peaks, so a powder
that mixes two or three phases shows all their peaks at once. Which phases are in
the powder? Scientists answer the question by searching a tree of phase sets: the
CrystalShift program (npj Computational Materials, 2025) did it on synchrotron data
from SSRL and CHESS, and the Dara program (Berkeley Lab, 2025) on the patterns of a
self-driving lab. Both report every set that explains the peaks about equally well,
because a scientist needs to know when the pattern alone cannot decide.

| Chess engine | Phase hunt |
| --- | --- |
| A position | The set of phases chosen so far |
| Legal moves | The library phases not in the set yet |
| make_move() and undo_move() | phases.append(name) and phases.pop() |
| Evaluation | Peaks explained, minus peaks left over, missing, and phases used |
| greedy_move() | Add the one phase that helps the score most, again and again |
| A search to a fixed depth | Score every set of up to three phases |
| Two move orders, one position | Quartz then rutile is the same set as rutile then quartz |
| Several moves with the best score | Several sets with the best score: the pattern cannot decide |
| Perft against python-chess | Known mixtures: does the search name the true phases? |

This file uses the standard library only and does not import the engine: it reuses
the engine's ideas, not its code.
"""

import random
from dataclasses import dataclass, field

TOLERANCE = 0.3  # Two peaks closer than this many degrees count as the same peak
MAX_PHASES = 3  # The most phases one powder may hold, which is the search depth
SEEN_CHANCE = 0.85  # The chance that a phase's peak shows up above the noise
SHIFT = 0.15  # A measured peak lands up to this many degrees from its true angle
EXPLAINED = 1  # Points for a measured peak that a chosen phase explains
LEFT_OVER = 1  # Points lost for a measured peak that no chosen phase explains
MISSING = 1  # Points lost for a predicted peak that the pattern does not show
PHASE_COST = 1  # Points lost for each phase, so a simpler explanation wins a tie
TRIALS = 200  # Powders in the benchmark
SILVER_POWDER = 12  # A benchmark powder of anatase and silver, a look-alike case

# The four strongest peaks of each phase, as 2-theta in degrees for copper X-rays
# (wavelength 1.5406 angstrom). Bragg's law turns each phase's published lattice
# size into these angles. Gold and silver have almost the same lattice size, so
# their peaks land less than 0.3 degrees apart.
LIBRARY = {
    "silicon": [28.4, 47.3, 56.1, 69.1],
    "halite": [31.7, 45.4, 56.5, 66.2],
    "quartz": [20.9, 26.6, 36.5, 50.1],
    "rutile": [27.4, 36.1, 41.2, 54.3],
    "anatase": [25.3, 37.8, 48.0, 55.1],
    "corundum": [25.6, 35.2, 43.4, 57.5],
    "zincite": [31.8, 34.4, 36.3, 56.6],
    "gold": [38.2, 44.4, 64.6, 77.6],
    "silver": [38.1, 44.3, 64.4, 77.4],
    "copper": [43.3, 50.4, 74.1, 89.9],
}
PHASE_NAMES = list(LIBRARY)  # The phases in library order, which the search follows

Phases = list[str]  # A set of phase names, such as ["quartz", "rutile"]


@dataclass
class Hunt:
    """What the search keeps while it runs."""

    score: int  # The best score found so far
    sets: list[Phases] = field(default_factory=list)  # Every set with that score
    nodes: int = 0  # Sets scored


def matches(peak: float, peaks: list[float]) -> bool:
    """Return True if some peak in peaks lies within TOLERANCE of this peak."""
    found = False
    for other in peaks:
        if abs(other - peak) <= TOLERANCE:
            found = True
    return found


def predicted_peaks(phases: Phases) -> list[float]:
    """Return every peak that the phases in the set would make, in one list."""
    peaks = []
    for name in phases:
        peaks += LIBRARY[name]  # Add the four peaks of this phase
    return peaks


def make_pattern(seed: int) -> tuple[list[float], Phases]:
    """
    Make the X-ray pattern of a powder that mixes one to three hidden phases.

    Parameters
    ----------
    seed : int
        The random seed, so the same seed always makes the same powder.

    Returns
    -------
    tuple[list[float], Phases]
        The measured peaks from low angle to high, and the true phases in
        alphabetical order. Each peak shows up with chance SEEN_CHANCE and lands
        up to SHIFT degrees from its true angle, the way real peaks do.
    """
    chooser = random.Random(seed)
    truth = chooser.sample(PHASE_NAMES, chooser.randint(1, MAX_PHASES))
    measured = []
    for name in truth:
        for peak in LIBRARY[name]:
            if chooser.random() < SEEN_CHANCE:
                measured.append(round(peak + chooser.uniform(-SHIFT, SHIFT), 2))
    return sorted(measured), sorted(truth)


def score(phases: Phases, measured: list[float]) -> int:
    """
    Evaluate a set of phases: how well does it explain the measured peaks?

    Parameters
    ----------
    phases : Phases
        The phases chosen so far, which may be none.
    measured : list[float]
        The peaks in the X-ray pattern.

    Returns
    -------
    int
        EXPLAINED points for each measured peak that one of the phases predicts,
        minus LEFT_OVER for each measured peak that none predicts, minus MISSING
        for each predicted peak the pattern does not show, minus PHASE_COST for
        each phase. A larger score is a better explanation.
    """
    predicted = predicted_peaks(phases)
    total = -PHASE_COST * len(phases)
    for peak in measured:
        if matches(peak, predicted):
            total += EXPLAINED
        else:
            total -= LEFT_OVER
    for peak in predicted:
        if not matches(peak, measured):
            total -= MISSING
    return total


def greedy_phases(measured: list[float]) -> Phases:
    """
    Build a set of phases one at a time, always adding the phase that raises the
    score most, the way greedy_move() always takes the biggest capture.

    Parameters
    ----------
    measured : list[float]
        The peaks in the X-ray pattern.

    Returns
    -------
    Phases
        The phases in the order they were added. The set stops growing when no
        phase raises the score, or when it holds MAX_PHASES phases.
    """
    phases = []
    while len(phases) < MAX_PHASES:
        best_name = None
        best_score = score(phases, measured)
        for name in PHASE_NAMES:
            if name in phases:
                continue
            phases.append(name)  # Try the phase, like making a move
            trial_score = score(phases, measured)
            phases.pop()  # Take it back, like undoing the move
            if trial_score > best_score:
                best_name = name
                best_score = trial_score
        if best_name is None:
            break
        phases.append(best_name)
    return phases


def search(
    phases: Phases, measured: list[float], depth: int, start: int, hunt: Hunt
) -> None:
    """
    Score this set of phases and every set that can grow from it, and keep every
    set that ties for the best score in hunt.

    Phases are added only in library order, from PHASE_NAMES[start] on. Quartz
    then rutile and rutile then quartz make the same set, so the search scores
    each set once instead of once for every order.

    Parameters
    ----------
    phases : Phases
        The phases chosen so far. The search adds and removes phases, and leaves
        the list as it found it.
    measured : list[float]
        The peaks in the X-ray pattern.
    depth : int
        How many more phases the set may take.
    start : int
        The index in PHASE_NAMES of the first phase the search may add.
    hunt : Hunt
        The best score so far and every set that earns it. The search adds one
        to hunt.nodes for each set it scores.
    """
    # Day 10, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 10 P3: write search()")


def run_search(measured: list[float]) -> Hunt:
    """Search every set of up to MAX_PHASES phases, starting from the empty set."""
    hunt = Hunt(score=score([], measured))
    search([], measured, MAX_PHASES, 0, hunt)
    return hunt


def search_answer(measured: list[float]) -> list[Phases]:
    """Return every set of phases that ties for the best score."""
    return run_search(measured).sets


def greedy_answer(measured: list[float]) -> list[Phases]:
    """Return the greedy set as the one and only answer."""
    return [greedy_phases(measured)]


def sets_every_order(depth: int) -> int:
    """
    Count the sets a search would score if it tried every order of the phases.

    With 10 phases and depth 3 the count is 1 + 10 + 10*9 + 10*9*8 = 821.
    """
    total = 1  # The empty set at the root
    layer = 1
    for level in range(depth):
        layer = layer * (len(PHASE_NAMES) - level)
        total += layer
    return total


def judge(answer: list[Phases], truth: Phases) -> str:
    """
    Compare an answer with the true phases.

    Returns
    -------
    str
        "right" when the answer is one set and it is the truth, "can't tell" when
        the truth is one of several sets that tie, and "wrong" otherwise.
    """
    truth_found = False
    for phases in answer:
        if sorted(phases) == truth:
            truth_found = True
    if not truth_found:
        return "wrong"
    if len(answer) == 1:
        return "right"
    return "can't tell"


def benchmark(strategy, trials: int = TRIALS) -> dict[str, int]:
    """
    Run a strategy on the benchmark powders and count its verdicts.

    Parameters
    ----------
    strategy : function
        Turns a list of measured peaks into a list of answer sets, such as
        greedy_answer or search_answer.
    trials : int
        The number of powders, made with seeds 0, 1, 2, ...

    Returns
    -------
    dict[str, int]
        How many powders got each verdict from judge().
    """
    counts = {"right": 0, "can't tell": 0, "wrong": 0}
    for seed in range(trials):
        measured, truth = make_pattern(seed)
        counts[judge(strategy(measured), truth)] += 1
    return counts


def show_benchmark(name: str, counts: dict[str, int]) -> None:
    """Print one strategy's verdicts on one line."""
    unsure = counts["can't tell"]
    print(
        f"  {name:6}: {counts['right']:3} right, {unsure:3} can't tell, "
        f"{counts['wrong']:3} wrong"
    )


def main():
    measured, truth = make_pattern(SILVER_POWDER)
    print(f"Powder {SILVER_POWDER} shows {len(measured)} peaks: {measured}")
    print(f"  True phases:  {truth}")
    print(f"  Greedy says:  {greedy_phases(measured)}")
    hunt = run_search(measured)
    print(f"  Search says:  {hunt.sets}, each with score {hunt.score}")
    print("  (expected: greedy names gold; the search finds gold or silver)")
    print(f"Benchmark: {TRIALS} powders of 1 to {MAX_PHASES} phases")
    show_benchmark("Greedy", benchmark(greedy_answer))
    show_benchmark("Search", benchmark(search_answer))
    print("  (expected: the search makes far fewer wrong calls than greedy)")
    print(
        f"Sets scored per powder: {hunt.nodes} in library order, "
        f"{sets_every_order(MAX_PHASES)} in every order  (expected: 176 and 821)"
    )


if __name__ == "__main__":
    main()
