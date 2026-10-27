# beam_time.py: Science AI: plan the beam time

*First appears in `instructor/Day 10 - Aim Remus at a science problem/period2`.*

## The big picture

A beamline shines X-rays on a sample, and every minute of beam time is precious.
Eight samples sit on the holder, and the scientists ask one question about each
one: is its signal above 50, which means a new crystal phase is there? Each
one-minute shot gives a noisy reading. There are only 40 shots for all eight
samples.

The agent chooses which sample to measure next, the way Remus chooses a move. A
sample that is clearly above or clearly below 50 needs few shots. A sample that is
too close to call gets more. This is the choice an AI agent makes on a real
beamline at Brookhaven's NSLS-II: where to spend the next minute.

## Where this piece fits

beam_time.py stands alone, like hidden_peak.py. It imports nothing from Remus. It borrows the engine's loop, not its code.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **shot:** one minute of X-rays on one sample, which gives one reading.
- **noise:** the random error in a reading. A dim sample gives noisy readings.
- **error:** how far the average of the readings may be from the true signal: the noise divided by the square root of the number of readings.
- **call:** the agent's answer for a sample, yes (above 50) or no.
- **gain:** how much one more shot is expected to lower the chance of a wrong call.

## What it stores

| Chess engine | Beam time agent |
| --- | --- |
| The board | The readings of each sample so far |
| Legal moves | The eight samples it could measure next |
| Make a move, look, undo it | Try three pretend readings, then forget them |
| Evaluation | The chance that each call is wrong |
| Perft against python-chess | Predicted wrong calls against real wrong calls |

| Agent | Wrong calls per holder, out of 8 |
| --- | --- |
| Random sample | about 0.94 |
| Equal time (5 shots each) | about 0.83 |
| Largest gain | about 0.65 |

## How it works

1. `make_samples()` fills a holder with eight hidden signals and their noise levels.
2. Each shot, the agent picks a sample, and `take_reading()` measures it.
3. `estimate()` turns the readings into an average and an error.
4. `chance_wrong()` and `expected_wrong_calls()` score how risky the calls are.
5. `gain()` looks one shot ahead, and `choose_next_sample()` picks the largest gain.
6. `benchmark()` runs each agent on 200 holders and compares wrong calls.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
choose_next_sample()
    gain()
        estimate()
        chance_wrong()

random_sample()

equal_time()

benchmark()
    make_samples()
    run_experiment()
        take_reading()
    expected_wrong_calls()
        chance_wrong()
        estimate()
    wrong_calls()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `make_samples` | Makes a holder of eight samples, each with a hidden signal and a noise level. | Day 10, period 2 |
| `take_reading` | Gives one noisy reading of a sample. | Day 10, period 2 |
| `estimate` | Averages the readings and works out their error. | Day 10, period 2 |
| `chance_wrong` | Gives the chance that the call for one sample is wrong. | Day 10, period 2 |
| `expected_wrong_calls` | Adds up the chances of a wrong call over all eight samples. | Day 10, period 2 |
| `gain` | Looks one shot ahead with three pretend readings and returns how much the risk drops. | Day 10, period 3 |
| `choose_next_sample` | Picks the sample whose next shot has the largest gain. | Day 10, period 3 |
| `random_sample` | Picks a sample at random: the agent that does not think. | Day 10, period 2 |
| `equal_time` | Gives every sample the same number of shots. | Day 10, period 2 |
| `run_experiment` | Spends all 40 shots on one holder and returns the readings. | Day 10, period 2 |
| `wrong_calls` | Counts the samples that got the wrong call. | Day 10, period 2 |
| `benchmark` | Runs one agent on 200 holders and reports the expected and real wrong calls. | Day 10, period 2 |

## How the file grows

- **Day 10, period 2:** `make_samples`, `take_reading`, `estimate`, `chance_wrong`, `expected_wrong_calls`, `random_sample`, `equal_time`, `run_experiment`, `wrong_calls`, `benchmark`
- **Day 10, period 3:** `gain`, `choose_next_sample`

## Try it

From inside a period folder that has the file, run:

```bash
uv run beam_time.py
```

You should see: The wrong calls per holder for the random, equal-time, and largest-gain agents, each next to the number the agent expected.

## Puzzle questions

1. A sample reads 51 after one shot, and another reads 90. Which one should get the next shot, and why?
2. Why does the agent try a reading one noise step low and one step high, and not only the average?
3. The agent's expected wrong calls land close to the real ones. Why does that matter to a scientist?

## Slides

Slides 10.5, 10.6, 10.7, 10.8 in the [slide plan](../slide_plan.md).
