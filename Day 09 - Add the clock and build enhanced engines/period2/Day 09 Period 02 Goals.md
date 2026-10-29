# Day 9, Period 2: Python lab 12 and the color versions

Each student pair builds one color version in `engines/student` at the top of the Remus folder, such as `engines/student/10 RED - Transposition table`. Each engine folder is a complete copy of Remus-WHITE, the `period1` engine, plus one enhancement.

## Learning objectives

By the end of this period, each student pair can:

- Use a dict as a cache with tuples as keys. **Measured by:** The lab remembers perft counts already computed and prints the time saved.
- Add one enhancement to Remus-WHITE. **Measured by:** The color version's own tests pass in its folder.

## The files

The lab is `python_caches.py` in the `student` folder, with the answers in `python_caches_instructor.py` in the `instructor` folder beside it. Open `python_caches.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Each student pair works in its own engine folder in `engines/student`, a complete copy of Remus-WHITE plus one enhancement. Remus-WHITE itself is in the `period1` folder.

## The changes and why

The student pairs fill in the blanks of `python_caches.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_caches_instructor.py`.

Part #1: `remembered_perft()` stores each knight path count in a dict under the tuple key `(square, depth)`. The second call finds the answer and returns at once. The RED color version's transposition table remembers search results the same way.

Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 to g7, which the CYAN color version needs, and `random.seed()`, which makes a random choice repeat on every run.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Student pairs work through `python_caches.py`: a dict remembers answers, `math.dist()`, and `random.seed()`. |
| 10:50 to 11:00 | Slides: the ten color versions. Each is Remus-WHITE plus one enhancement, such as RED (transposition table) or BLUE (killer moves). Colors name the color versions so that no color version sounds better than another. |
| 11:00 to 12:00 | Each student pair opens its color version in `engines/student`, reads the version README, and writes the color version's stubbed code. |

## What you edit in the lab

Open `python_caches.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 7. Check the work by running `python_caches.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
