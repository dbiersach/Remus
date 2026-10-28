# phase_hunt.py: Science AI: name the crystals in a powder

*First appears in `Day 10 - Solve a science problem using chess AI/period2/instructor`.*

## The big picture

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

## Where this piece fits

phase_hunt.py stands alone, like hidden_peak.py. It imports nothing from Remus. It borrows the engine's search, not its code.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **phase:** one kind of crystal, such as quartz. A powder can mix several phases.
- **peak:** a bright spot in the X-ray pattern, at an angle called 2-theta. Each phase has its own set of peaks.
- **fingerprint:** the list of a phase's peaks. Bragg's law turns the size of the crystal's repeating cell into these angles.
- **tolerance:** how close two peaks must be, 0.3 degrees, to count as the same peak.
- **can't tell:** the verdict when several sets of phases tie for the best score, such as gold and silver, whose peaks overlap.

## What it stores

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

## How it works

1. `make_pattern()` mixes one to three hidden phases. Each peak shows up 85 times in 100 and lands up to 0.15 degrees from its true angle.
2. `score()` checks every measured peak and every predicted peak and adds up the points.
3. `greedy_phases()` adds the phase that raises the score most until no phase helps.
4. `search()` scores the set it is given, keeps every set that ties for the best, and calls itself with one more phase, adding phases in library order only.
5. `judge()` compares an answer with the true phases: right, can't tell, or wrong.
6. `benchmark()` runs an agent on 200 powders and counts the verdicts.

## Call tree

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

## The functions

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

## How the file grows

- **Day 10, period 2:** `matches`, `predicted_peaks`, `make_pattern`, `score`, `greedy_phases`, `greedy_answer`, `judge`, `benchmark`, `show_benchmark`
- **Day 10, period 3:** `Hunt`, `search`, `run_search`, `search_answer`, `sets_every_order`

## Try it

Open `phase_hunt.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A powder of anatase and silver that greedy names as anatase and gold, the search's two tied answers, the verdicts of both agents over 200 powders, and 176 sets scored against 821.

## Puzzle questions

1. A guess explains every peak but uses one phase more than another guess that also explains every peak. Which guess scores higher, and why?
2. Why does greedy name gold for a powder that holds silver, and what does the search say instead?
3. Greedy names more powders right than the search does. Why would a scientist still rather use the search?
4. Why does adding phases in library order give the same answer as trying every order?

## Slides

Slides 10.5, 10.6, 10.7, 10.8 in the [slide plan](../course/slide_plan.md).
