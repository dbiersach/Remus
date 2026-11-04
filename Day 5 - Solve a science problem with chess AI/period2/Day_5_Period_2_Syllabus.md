# Day 5, Period 2: Name the crystals, the greedy way

10:30 to 12:00. Part of [Day 5: The science project](../Day_5_Syllabus.md).

## Goal

The student pair scores a set of crystal phases and builds the greedy answer.

## The big picture

No engine file changes today: `engines/Remus1` to `engines/Remus4` stay as they were at the end of Day 4. The student pair writes `score()` and `greedy_phases()` in `phase_hunt.py`, a science program that reuses the engine's ideas, not its code: `score()` is the evaluation of a set of phases, and `greedy_phases()` is a one-move-deep search that keeps adding the best phase. `phase_hunt.py` holds every other line already, so the student pair types only the bodies of these functions, from their docstrings. The student pair edits `science/phase_hunt.py`, and `science_instructor/phase_hunt.py` holds the finished version.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | The PDF beamline at Brookhaven's NSLS-II and its daily question: which crystal phases are in this powder? Each phase makes its own fingerprint of X-ray peaks. |
| 10:45 to 11:15 | Write `score()` in `phase_hunt.py` (11 code lines): a point for each explained peak, and a point lost for each left-over peak, missing peak, and phase used. |
| 11:15 to 12:00 | Write `greedy_phases()` (16 lines), which adds the best phase again and again. On 200 known powders greedy names 166 right and 34 wrong, and on powder 12 it mistakes silver for gold. |

## The files

| File | The instructor's version |
| --- | --- |
| `phase_hunt.py` | [`science_instructor/phase_hunt.py`](../../science_instructor/phase_hunt.py) |

### `phase_hunt.py`

These images show the function bodies from [`science_instructor/phase_hunt.py`](../../science_instructor/phase_hunt.py). In `science/phase_hunt.py`, replace the comment and the `raise` line under each docstring with the body. Work from the top of the file down, and the line numbers match when you reach each function.

![score(), lines 140 to 150](images/phase_hunt_lines_140_to_150.png)

![greedy_phases(), lines 170 to 185](images/phase_hunt_lines_170_to_185.png)

### The graphs

When `phase_hunt.py` finishes the greedy benchmark, matplotlib opens this graph of powder 12. Close the window and the program continues, until it stops at "Write search()", the function of Period 3. The student pair types none of the graph code.

![Powder 12 and the greedy answer](images/powder_answer.png)

These pictures explain the experiment and the two functions of this period.

![The experiment at the beamline](images/experiment.png)

![The fingerprint of each phase](images/fingerprints.png)

![The mystery powder](images/mystery_powder.png)

![Three guesses scored peak by peak](images/scoring.png)

![Greedy, step by step](images/greedy_steps.png)

## Done when

`greedy_phases()` runs on the 200 known powders and prints its right and wrong counts.
