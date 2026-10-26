# hidden_peak.py

Science AI: chooses where to measure next to find a hidden hot spot.

First appears in `Day 10 - Upgrade Remus and add Science AI`.

## What it does

A 10x10 sample hides a hot spot that reads 100, fading to 0 with distance. Every
measurement costs time, so the goal is to find the peak in as few measurements as
possible: the same choice an autonomous agent makes at a beamline at Brookhaven's
NSLS-II.

## The map from chess

| Chess engine | Hidden peak |
| --- | --- |
| Legal moves | `candidate_squares`: squares not yet measured |
| `make_move`, `undo_move` | Add a pretend reading, then delete it |
| Evaluation | `score_candidate`: predicted value (exploit) plus `EXPLORE_WEIGHT` times the distance to the nearest reading (explore) |
| `greedy_move` | `choose_next_measurement` |
| Minimax | `expectimax_choice`: average a high and a low reading, because nature is not an opponent |
| A match | `benchmark`: average measurements over 100 hidden samples |

## Results

| Strategy | Average measurements |
| --- | --- |
| Random guessing | about 54 |
| Greedy, explore weight 0 | about 18 |
| Greedy, explore weight 8 | about 9 |
| Greedy, explore weight 40 | about 19 |
| Expectimax, depth 2 | about 23 to 32 |

The greedy AI with a moderate exploration term wins. Expectimax does worse because its
"plus or minus 20" guess is a crude model of uncertainty; the NSLS-II agent uses a
Gaussian process, which knows how uncertain each prediction is. The file uses only the
standard library and reuses the engine's ideas, not its code. `main()` takes about a
minute.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `make_grid` | 10 | Make a hidden sample: a hot spot at a random square, fading with distance. |
| `measure` | 10 | Return the reading at one square of the hidden sample. |
| `predicted_value` | 10 | Predict the reading at a square from the readings so far. |
| `candidate_squares` | 10 | Return every square not yet measured, the "legal moves" of this problem. |
| `score_candidate` | 10 | Score a square as the next measurement, the "evaluation" of this problem. |
| `choose_next_measurement` | 10 | Return the unmeasured square with the highest score, like greedy_move(). |
| `random_strategy` | 10 | Measure a random unmeasured square, the baseline every AI must beat. |
| `expectimax_choice` | 10 | Look two measurements ahead (teacher demo). |
| `measurements_to_find_peak` | 10 | Run one strategy on one sample and count measurements until it reads PEAK. |
| `benchmark` | 10 | Return the average number of measurements a strategy needs over many samples. |

## Try it

From inside a Day folder that has the file:

```bash
uv run hidden_peak.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 10.11, 10.12, 10.13, 10.14, 10.15.
