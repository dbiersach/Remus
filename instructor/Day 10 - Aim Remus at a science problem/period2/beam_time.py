#!/usr/bin/env -S uv run
"""beam_time.py

Spend a short block of beamline time where it teaches the most, with the same loop
that chooses a chess move.

A sample holder at a beamline carries eight samples. For each sample the scientists
ask one yes-or-no question: is its signal above THRESHOLD, which means a new crystal
phase is present? Every one-minute shot of X-rays gives a reading of the signal plus
random noise. A dim sample gives noisy readings, and a bright sample gives clean ones,
and the label on each sample says how noisy it is. The beam time is short: 40 shots
for all eight samples. After each shot the agent chooses which sample to measure
next. When the time runs out it calls every sample "yes" or "no", and the score is
the number of correct calls.

The agent runs the loop Remus runs:

1. Represent: the readings taken so far, one list per sample (Remus: the board).
2. Generate: the samples it could measure next (Remus: the legal moves).
3. Look ahead: try pretend readings of a sample and predict how much one more
   shot would help (Remus: make a move, look at the position, undo it).
4. Evaluate: the chance that each call is wrong (Remus: the evaluation).
5. Verify: compare the wrong calls the agent predicts with the wrong calls it
   really makes (Remus: perft against python-chess).

The NSLS-II agent at Brookhaven makes the same choice with a statistical model of
the sample in place of this hand-built one.
"""

import math
import random

SAMPLES = 8  # Samples on the holder
SHOTS = 40  # One-minute shots of beam time for the whole holder
THRESHOLD = 50.0  # A signal above this means the new phase is present
NOISE_LEVELS = [5.0, 10.0, 20.0, 40.0]  # Bright samples have small noise
TRIALS = 200  # Sample holders in the benchmark

Readings = list[list[float]]  # Readings[i] holds every reading of sample i


def make_samples(seed: int) -> list[dict[str, float]]:
    """
    Make a sample holder with hidden signals and known noise levels.

    Parameters
    ----------
    seed : int
        The random seed, so the same seed always makes the same holder.

    Returns
    -------
    list[dict[str, float]]
        One dict per sample with its hidden "signal" and its "noise" level.
    """
    rng = random.Random(seed)
    samples = []
    for _ in range(SAMPLES):
        samples.append(
            {"signal": rng.uniform(20.0, 80.0), "noise": rng.choice(NOISE_LEVELS)}
        )
    return samples


def take_reading(sample: dict[str, float], rng: random.Random) -> float:
    """Return one noisy reading of a sample: its signal plus random noise."""
    return rng.gauss(sample["signal"], sample["noise"])


def estimate(readings: list[float], noise: float) -> tuple[float, float]:
    """
    Estimate a sample's signal from its readings.

    Parameters
    ----------
    readings : list[float]
        Every reading of the sample, at least one.
    noise : float
        The noise level of one reading.

    Returns
    -------
    tuple[float, float]
        The average reading, and its error: noise / sqrt(number of readings).
        Four readings cut the error in half.
    """
    average = sum(readings) / len(readings)
    error = noise / math.sqrt(len(readings))
    return average, error


def chance_wrong(average: float, error: float) -> float:
    """
    Return the chance that the call for a sample is wrong.

    The true signal lies near the average, within about one error either side.
    An average far from THRESHOLD, measured in errors, gives a safe call; an
    average right at THRESHOLD is a coin flip, with a chance of 0.5.
    """
    distance = abs(average - THRESHOLD) / error  # How many errors from the line
    return 0.5 * math.erfc(distance / math.sqrt(2))  # The tail of a bell curve


def expected_wrong_calls(readings: Readings, noises: list[float]) -> float:
    """
    Evaluate the experiment so far: the number of wrong calls to expect.

    Parameters
    ----------
    readings : Readings
        The readings of every sample.
    noises : list[float]
        The noise level of every sample.

    Returns
    -------
    float
        The sum of chance_wrong() over the samples. A sample with no readings
        yet adds 0.5, because its call is a coin flip.
    """
    total = 0.0
    for sample_readings, noise in zip(readings, noises, strict=True):
        if not sample_readings:
            total += 0.5
            continue
        total += chance_wrong(*estimate(sample_readings, noise))
    return total


def random_sample(readings: Readings, noises: list[float]) -> int:
    """Return a random sample: an agent that does not think."""
    return random.randrange(SAMPLES)


def equal_time(readings: Readings, noises: list[float]) -> int:
    """Return the sample with the fewest readings, so every sample gets 5 shots."""
    fewest = 0
    for sample in range(SAMPLES):
        if len(readings[sample]) < len(readings[fewest]):
            fewest = sample
    return fewest


def run_experiment(samples: list[dict[str, float]], strategy, seed: int) -> Readings:
    """
    Spend all the beam time on one sample holder and return the readings.

    Parameters
    ----------
    samples : list[dict[str, float]]
        The sample holder, from make_samples().
    strategy : function
        Chooses the next sample from (readings, noises), such as
        choose_next_sample.
    seed : int
        The random seed for the noise in the readings.
    """
    rng = random.Random(seed)
    noises = []
    readings = []
    for sample in samples:
        noises.append(sample["noise"])
        readings.append([])  # No shots on this sample yet
    for _ in range(SHOTS):
        choice = strategy(readings, noises)
        readings[choice].append(take_reading(samples[choice], rng))
    return readings


def wrong_calls(samples: list[dict[str, float]], readings: Readings) -> int:
    """Return how many samples get the wrong call; a sample never measured is wrong."""
    wrong = 0
    for sample, sample_readings in zip(samples, readings, strict=True):
        if not sample_readings:
            wrong += 1
            continue
        says_yes = sum(sample_readings) / len(sample_readings) > THRESHOLD
        if says_yes != (sample["signal"] > THRESHOLD):
            wrong += 1
    return wrong


def benchmark(strategy, trials: int = TRIALS) -> tuple[float, float]:
    """
    Run a strategy on many sample holders.

    Returns
    -------
    tuple[float, float]
        The average wrong calls per holder the agent expected at the end
        (from expected_wrong_calls), and the average it really made.
    """
    random.seed(2016)  # The random strategy gives the same result on every run
    expected, real = 0.0, 0
    for trial in range(trials):
        samples = make_samples(trial)
        readings = run_experiment(samples, strategy, seed=trial + 10_000)
        noises = []
        for sample in samples:
            noises.append(sample["noise"])
        expected += expected_wrong_calls(readings, noises)
        real += wrong_calls(samples, readings)
    return expected / trials, real / trials


def main():
    print(f"Beam time: {SHOTS} shots for {SAMPLES} samples, on {TRIALS} holders")
    for name, strategy in [
        ("Random sample", random_sample),
        ("Equal time", equal_time),
    ]:
        expected, real = benchmark(strategy)
        print(
            f"  {name:13}: {real:.2f} wrong calls per holder "
            f"(the agent expected {expected:.2f})"
        )
    print("  (expected: equal time makes fewer wrong calls than random samples)")


if __name__ == "__main__":
    main()
