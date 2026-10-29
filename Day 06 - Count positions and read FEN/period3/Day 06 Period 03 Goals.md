# Day 6, Period 3: Perft against python-chess, and bug hunt

The `bug_hunt` folder holds a copy of this period's Remus with three planted bugs. Running `hunt.py` inside it shows where the counts go wrong.

## Learning objectives

By the end of this period, each pair can:

- Compare Remus with python-chess on standard positions. **Measured by:** `test_perft.py` passes on all five positions.
- Find a planted bug with `divide()`. **Measured by:** Running `hunt.py` in `bug_hunt/` points at three bugs; the pair fixes at least two of them and names the root move that showed each one.

## The files

New files this period:

- `test_perft.py`

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: `test_perft.py` compares Remus with python-chess on the standard positions. |
| 1:15 to 2:10 | Bug hunt: the `bug_hunt` folder holds a copy of Remus with three planted bugs. Pairs run `hunt.py` there and race to find each bug from the root moves whose counts disagree. |
| 2:10 to 2:25 | Pairs explain each bug they found and the rule it broke. |
| 2:25 to 2:30 | Wrap-up: the hunt is over when `hunt.py` prints 0 root moves that disagree. |

## What you edit in the bug hunt

Open the `bug_hunt` folder inside `student` and run `hunt.py` there in VS Code. Each root move it prints points at a planted bug in one of the Remus files of that folder. Fix each bug by changing the line that breaks the rule, and run the hunt again until every count agrees. The files outside `bug_hunt` are correct, so compare with them only after a guess.

Lines to fix in all: 3. `bug_hunt/README.md` explains the hunt.
