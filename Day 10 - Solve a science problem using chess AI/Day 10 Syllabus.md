# Day 10: Solve a science problem using chess AI

Day 10 aims the engine's ideas at real science. The same generate, score, and choose loop picks where to measure a hidden peak, and the full tree search, with make and undo, names the crystal phases in an X-ray powder pattern. The day ends with each pair reporting its science results, and every pair takes its code home.

## Objectives for the day

By 4:30, each pair can:

- Map the parts of a chess engine onto a science problem: moves, make and undo, evaluation, and search.
- Choose the next measurement by trading off exploring the unknown against exploiting what the readings predict.
- Score a guess about which phases are in a powder, and compare a greedy agent with a full search.
- Verify a search on known answers, and say when the right answer is "can't tell".
- Report a science result with its counts, and explain one decision the science AI made.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Science AI: hidden_peak.py | `candidate_squares()` in `hidden_peak.py` (6 lines); `score_candidate()` in `hidden_peak.py` (4 lines); `choose_next_measurement()` in `hidden_peak.py` (9 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | The phase hunt: score a guess, and the greedy agent | `score()` in `phase_hunt.py` (11 lines); `greedy_phases()` in `phase_hunt.py` (17 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | The phase hunt: search every set, and verify | `search()` in `phase_hunt.py` (13 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Science results, take-home, and wrap-up | Nothing: teacher code |

## Period 1, 8:30 to 10:00: Science AI: hidden_peak.py

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Unplugged warm-up, "Find the hidden peak": a 10x10 grid hides a hot spot, and each pair gets five measurements to find it. |
| 8:45 to 8:55 | Slides: the map from chess to science. Legal moves become squares not yet measured, and the evaluation becomes predicted value plus distance to the nearest reading. |
| 8:55 to 9:35 | Pairs write `candidate_squares()`, `score_candidate()`, and `choose_next_measurement()` in `hidden_peak.py`. |
| 9:35 to 10:00 | Pairs tune `explore_weight` and post their 100-grid benchmark average on the board, next to random guessing. |

[`Day 10 Period 01 Goals.md`](<period1/Day 10 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: The phase hunt: score a guess, and the greedy agent

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | A scientist (or the teacher) shows the NSLS-II PDF beamline and its daily question: which crystal phases are in this powder? |
| 10:45 to 11:00 | Unplugged warm-up, "Name the powder": pairs lay paper fingerprint strips over a printed mystery pattern. |
| 11:00 to 11:25 | Pairs write `score()` in `phase_hunt.py`: a point for each explained peak, and a point lost for each extra peak, missing peak, and phase used. |
| 11:25 to 12:00 | Pairs write `greedy_phases()`, which adds the best phase again and again with `append` and `pop`. Greedy names 166 of 200 powders right and 34 wrong, and it mistakes silver for gold. |

[`Day 10 Period 02 Goals.md`](<period2/Day 10 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: The phase hunt: search every set, and verify

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | The teacher draws the tree of phase sets next to Remus's game tree: a set is a position, adding a phase is a move, and taking it back is the undo. |
| 1:15 to 1:50 | Pairs write `search()`, which scores every set of up to three phases and keeps every set that ties for the best score. |
| 1:50 to 2:15 | The class verifies on 200 known powders: 139 right, 52 "can't tell", and 9 wrong, against greedy's 34 wrong. Pairs change `PHASE_COST` and `MISSING` and watch the verdicts move. |
| 2:15 to 2:30 | The teacher closes with the programs that search the same tree on real synchrotron data, and the beamline agent at Brookhaven. |

[`Day 10 Period 03 Goals.md`](<period3/Day 10 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Science results, take-home, and wrap-up

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Each student copies the pair's repository to a USB drive with `git clone --no-hardlinks` and checks that the copy opens and runs `uv run pytest`. |
| 3:15 to 3:40 | Each pair runs `hidden_peak.py` and `phase_hunt.py` once more and fills in its results table: measurements against random guessing, and right, wrong, and can't-tell counts for greedy and for search. The class collects every pair's numbers on the board. |
| 3:40 to 3:55 | Each pair picks one powder its search named and one it answered with can't tell, and works out which measurement would settle the second. |
| 3:55 to 4:20 | Each pair presents its results and its two powders in three minutes. |
| 4:20 to 4:30 | The class closes with what comes next: AI agents that steer real experiments at light sources such as NSLS-II. |

[`Day 10 Period 04 Goals.md`](<period4/Day 10 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Every pair's `choose_next_measurement()` beats random guessing, every pair's `search()` makes fewer wrong calls than greedy, and every pair has reported its results and taken its code home.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
