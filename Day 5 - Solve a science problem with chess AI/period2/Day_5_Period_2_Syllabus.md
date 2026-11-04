# Day 5, Period 2: Name the crystals, the greedy way

10:30 to 12:00. Part of [Day 5: The science project](../Day_5_Syllabus.md).

## Goal

The student pair scores a set of crystal phases and builds the greedy answer.

## The big picture

No engine file changes today: `engines/Remus1` to `engines/Remus4` stay as they were at the end of Day 4. The student pair writes `score()` and `greedy_phases()` in `phase_hunt.py`, a science program that reuses the engine's ideas, not its code: `score()` is the evaluation of a set of phases, and `greedy_phases()` is a one-move-deep search that keeps adding the best phase. `phase_hunt.py` holds every other line already, so the student pair types only the bodies of these functions, from their docstrings. The student pair edits `science/student/phase_hunt.py`, and `science/instructor/phase_hunt.py` holds the finished version.

## The files

| File | The instructor's version |
| --- | --- |
| phase_hunt.py | Not in the repository yet |

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | The PDF beamline at Brookhaven's NSLS-II and its daily question: which crystal phases are in this powder? Each phase makes its own fingerprint of X-ray peaks. |
| 10:45 to 11:15 | Write `score()` in `phase_hunt.py` (11 code lines): a point for each explained peak, and a point lost for each left-over peak, missing peak, and phase used. |
| 11:15 to 12:00 | Write `greedy_phases()` (17 code lines), which adds the best phase again and again. On 200 known powders greedy names 166 right and 34 wrong, and on powder 12 it mistakes silver for gold. |

## Done when

`greedy_phases()` runs on the 200 known powders and prints its right and wrong counts.
