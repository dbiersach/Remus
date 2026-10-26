# hidden_peak.py: Science AI: find the hidden peak

*First appears in `instructor/Day 10 - Upgrade Remus and add Science AI`.*

## The big picture

A science sample hides a hot spot. Each measurement takes time, so we want to find
the hot spot in as few measurements as we can.

This file uses the same idea as the chess engine. List the choices. Score each one.
Pick the best. Here the choices are squares to measure, not moves.

## Where this piece fits

hidden_peak.py stands alone. It imports nothing from Remus. It borrows the engine's ideas, not its code.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **measurement:** reading the value at one square of the sample.
- **exploit:** measure where it already looks hot.
- **explore:** measure somewhere new, far from earlier readings.
- **benchmark:** a fair test: run each method on the same 100 samples and compare averages.
- **expectimax:** like minimax, but it averages the outcomes, because nature is not an opponent.

## What it stores

| Chess engine | Hidden peak |
| --- | --- |
| Legal moves | Squares not measured yet |
| Evaluation | Predicted value plus a bonus for exploring |
| `greedy_move()` | Measure the best-scoring square |
| Minimax | Expectimax: average a high and a low reading |
| A match | A benchmark over 100 samples |

| Method | Average measurements |
| --- | --- |
| Random guessing | about 54 |
| Greedy AI, explore weight 8 | about 9 |

## How it works

1. `make_grid()` hides a hot spot on a 10x10 grid.
2. Every method starts by measuring the center.
3. `candidate_squares()` lists the squares not measured yet.
4. `score_candidate()` adds the predicted value and an explore bonus.
5. `choose_next_measurement()` picks the highest score.
6. `benchmark()` repeats this on 100 samples and averages the count.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
choose_next_measurement()
    candidate_squares()
    score_candidate()
        predicted_value()

random_strategy()
    candidate_squares()

expectimax_choice()
    candidate_squares()
    predicted_value()
    score_candidate()
        predicted_value()

benchmark()
    measurements_to_find_peak()
        measure()
    make_grid()
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `make_grid` | Hides a hot spot on a 10x10 grid. | 10 |
| `measure` | Reads the value at one square. | 10 |
| `predicted_value` | Guesses a square's value from the readings so far. | 10 |
| `candidate_squares` | Lists the squares not measured yet. | 10 |
| `score_candidate` | Scores a square: predicted value plus an explore bonus. | 10 |
| `choose_next_measurement` | Picks the square with the best score. | 10 |
| `random_strategy` | Picks a random square. Every AI must beat it. | 10 |
| `expectimax_choice` | Looks two measurements ahead and averages the outcomes. | 10 |
| `measurements_to_find_peak` | Counts measurements until one method finds the peak. | 10 |
| `benchmark` | Averages that count over many hidden samples. | 10 |

## Try it

From inside a Day folder that has the file, run:

```bash
uv run hidden_peak.py
```

You should see: The average for random guessing, three greedy AIs, and the expectimax AI. It takes about a minute.

## Puzzle questions

1. What happens with explore weight 0? With 40? Why?
2. How is `candidate_squares()` like `legal_moves()`?

## Slides

Slides 10.11, 10.12, 10.13, 10.14, 10.15 in the [slide plan](../slide_plan.md).
