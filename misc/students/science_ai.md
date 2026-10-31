# Science AI: the Day 10 files

On Day 10 the same loop that picks a chess move, list the candidates, score each one,
and choose the best, aims at two science problems. `hidden_peak.py` chooses where to
measure next on a 10x10 sample, and `phase_hunt.py` searches a tree of crystal
phases to name the ones in a powder, the way a beamline program does. Neither file
imports the engine: they reuse its ideas, not its code. This page has one section per
file.

| File | When | Page section |
| --- | --- | --- |
| `hidden_peak.py` | Day 10, period 1 | [Science AI: find the hidden peak](#hidden_peakpy-science-ai-find-the-hidden-peak) |
| `phase_hunt.py` | Day 10, periods 2 and 3 | [Science AI: name the crystals in a powder](#phase_huntpy-science-ai-name-the-crystals-in-a-powder) |

## hidden_peak.py: Science AI: find the hidden peak

*First appears in `Day 10 - Solve a science problem using chess AI/period1/instructor`.*

### The big picture

A science sample hides a hot spot. Each measurement takes time, so we want to find
the hot spot in as few measurements as we can.

This file uses the same idea as the chess engine. List the choices. Score each one.
Pick the best. Here the choices are squares to measure, not moves.

### Where this piece fits

hidden_peak.py stands alone. It imports nothing from Remus. It borrows the engine's ideas, not its code.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

### Words to know

- **measurement:** reading the value at one square of the sample.
- **exploit:** measure where it already looks hot.
- **explore:** measure somewhere new, far from earlier readings.
- **benchmark:** a fair test: run each method on the same 100 samples and compare averages.
- **expectimax:** like minimax, but it averages the outcomes, because nature is not an opponent.

### What it stores

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

### How it works

1. `make_grid()` hides a hot spot on a 10x10 grid.
2. Every method starts by measuring the center.
3. `candidate_squares()` lists the squares not measured yet.
4. `score_candidate()` adds the predicted value and an explore bonus.
5. `choose_next_measurement()` picks the highest score.
6. `benchmark()` repeats this on 100 samples and averages the count.

### Call tree

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

### The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `make_grid` | Hides a hot spot on a 10x10 grid. | Day 10, period 1 |
| `measure` | Reads the value at one square. | Day 10, period 1 |
| `predicted_value` | Guesses a square's value from the readings so far. | Day 10, period 1 |
| `candidate_squares` | Lists the squares not measured yet. | Day 10, period 1 |
| `score_candidate` | Scores a square: predicted value plus an explore bonus. | Day 10, period 1 |
| `choose_next_measurement` | Picks the square with the best score. | Day 10, period 1 |
| `random_strategy` | Picks a random square. Every AI must beat it. | Day 10, period 1 |
| `expectimax_choice` | Looks two measurements ahead and averages the outcomes. | Day 10, period 1 |
| `measurements_to_find_peak` | Counts measurements until one method finds the peak. | Day 10, period 1 |
| `benchmark` | Averages that count over many hidden samples. | Day 10, period 1 |

### Try it

Open `hidden_peak.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: The average for random guessing, three greedy AIs, and the expectimax AI. It takes about a minute.

### Puzzle questions

1. What happens with explore weight 0? With 40? Why?
2. How is `candidate_squares()` like `legal_moves()`?

### Slides

Slides 10.1, 10.2, 10.3, 10.4, 10.9 in the [slide plan](../teachers/slide_plan.md).

## phase_hunt.py: Science AI: name the crystals in a powder

*First appears in `Day 10 - Solve a science problem using chess AI/period2/instructor`.*

### The big picture

A beamline such as the PDF beamline at Brookhaven's NSLS-II shines X-rays
through a powder. The detector records peaks, each at an angle. Every crystal
phase (silicon, quartz, rutile, and so on) makes its own fingerprint of peaks, so a
powder that mixes two or three phases shows all their peaks at once. Which phases
are in the powder?

The phase hunt answers the question the way Remus picks a move. It tries adding a
phase, scores how well the set explains the peaks, takes the phase back, and
searches every set of up to three phases. Real programs search the same tree:
CrystalShift on synchrotron data from SSRL and CHESS, and Dara on the patterns of
a self-driving lab at Berkeley Lab. Like them, the phase hunt keeps every answer
that ties for the best score, because a scientist needs to know when the pattern
alone cannot decide.

### Where this piece fits

phase_hunt.py stands alone, like hidden_peak.py. It imports nothing from Remus. It borrows the engine's search, not its code.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

### Words to know

- **phase:** one kind of crystal, such as quartz. A powder can mix several phases.
- **peak:** a bright spot in the X-ray pattern, at an angle called 2-theta. Each phase has its own set of peaks.
- **fingerprint:** the list of a phase's peaks. Bragg's law turns the size of the crystal's repeating cell into these angles.
- **tolerance:** how close two peaks must be, 0.3 degrees, to count as the same peak.
- **can't tell:** the verdict when several sets of phases tie for the best score, such as gold and silver, whose peaks overlap.

### What it stores

| Chess engine | Phase hunt |
| --- | --- |
| A position | The set of phases chosen so far |
| Legal moves | The library phases not in the set yet |
| Make a move, undo it | `phases.append(name)`, `phases.pop()` |
| Evaluation | Peaks explained, minus peaks left over, missing, and phases used |
| `greedy_move()` | `greedy_phases()`: add the best phase again and again |
| Two move orders, one position | Quartz then rutile is the same set as rutile then quartz |
| Perft against python-chess | 200 powders whose true phases are known |

| Agent | Right | Can't tell | Wrong |
| --- | --- | --- | --- |
| Greedy | 166 | 0 | 34 |
| Search | 139 | 52 | 9 |

### How it works

1. `make_pattern()` mixes one to three hidden phases. Each peak shows up 85 times in 100 and lands up to 0.15 degrees from its true angle.
2. `score()` checks every measured peak and every predicted peak and adds up the points.
3. `greedy_phases()` adds the phase that raises the score most until no phase helps.
4. `search()` scores the set it is given, keeps every set that ties for the best, and calls itself with one more phase, adding phases in library order only.
5. `judge()` compares an answer with the true phases: right, can't tell, or wrong.
6. `benchmark()` runs an agent on 200 powders and counts the verdicts.

### Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
search_answer()
    run_search()
        Hunt()
        search()
            score()
                predicted_peaks()
                matches()
            Hunt()
            search()  (calls itself again, one move deeper)
        score()
            predicted_peaks()
            matches()

greedy_answer()
    greedy_phases()
        score()
            predicted_peaks()
            matches()

sets_every_order()

benchmark()
    make_pattern()
    judge()

show_benchmark()
```

### The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `Hunt` | Holds what the search keeps: the best score, every set with that score, and the number of sets scored. | Day 10, period 3 |
| `matches` | Says whether a peak lies within 0.3 degrees of any peak in a list. | Day 10, period 2 |
| `predicted_peaks` | Puts the peaks of every phase in a set into one list. | Day 10, period 2 |
| `make_pattern` | Makes the X-ray pattern of a powder of one to three hidden phases. | Day 10, period 2 |
| `score` | Scores a set of phases: explained peaks, minus peaks left over, missing peaks, and phases used. | Day 10, period 2 |
| `greedy_phases` | Adds the best phase again and again, like greedy_move(). | Day 10, period 2 |
| `search` | Scores every set of up to three phases with append and pop, and keeps every set that ties for the best. | Day 10, period 3 |
| `run_search` | Starts the search from the empty set. | Day 10, period 3 |
| `search_answer` | Returns every set that ties for the best score. | Day 10, period 3 |
| `greedy_answer` | Returns the greedy set as the only answer. | Day 10, period 2 |
| `sets_every_order` | Counts the sets a search would score if it tried every order of the phases: 821. | Day 10, period 3 |
| `judge` | Calls an answer right, can't tell, or wrong. | Day 10, period 2 |
| `benchmark` | Runs one agent on 200 powders and counts its verdicts. | Day 10, period 2 |
| `show_benchmark` | Prints one agent's verdicts on one line. | Day 10, period 2 |

### How the file grows

- **Day 10, period 2:** `matches`, `predicted_peaks`, `make_pattern`, `score`, `greedy_phases`, `greedy_answer`, `judge`, `benchmark`, `show_benchmark`
- **Day 10, period 3:** `Hunt`, `search`, `run_search`, `search_answer`, `sets_every_order`

### Try it

Open `phase_hunt.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A powder of anatase and silver that greedy names as anatase and gold, the search's two tied answers, the verdicts of both agents over 200 powders, and 176 sets scored against 821.

### Puzzle questions

1. A guess explains every peak but uses one phase more than another guess that also explains every peak. Which guess scores higher, and why?
2. Why does greedy name gold for a powder that holds silver, and what does the search say instead?
3. Greedy names more powders right than the search does. Why would a scientist still rather use the search?
4. Why does adding phases in library order give the same answer as trying every order?

### Slides

Slides 10.5, 10.6, 10.7, 10.8 in the [slide plan](../teachers/slide_plan.md).
