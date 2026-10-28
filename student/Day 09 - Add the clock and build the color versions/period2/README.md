# Day 9, Period 2: Python lab 12 and the color versions

Each pair builds one color version in the `Remus` folder next to the Day folders, such as `10 RED - Transposition table`. The code in this Day folder is Remus-WHITE, the starting point of every color version.

## Learning objectives

By the end of this period, each pair can:

- Use a dict as a cache with tuples as keys. **Measured by:** The lab remembers perft counts already computed and prints the time saved.
- Add one enhancement to Remus-WHITE. **Measured by:** The color version's own tests pass in its folder.

## The files

The lab is `python_caches.py` in `student/`, with the answers in `python_caches_instructor.py` in `instructor/`. Open `python_caches.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_caches.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_caches_instructor.py`.

Part #1: `remembered_perft()` stores each answer in a dict under the tuple key `(name, depth)`. The second call finds the answer and returns at once. The RED color version's transposition table remembers search results the same way.

Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 to g7, which the CYAN color version needs, and `random.seed()`, which makes a random choice repeat on every run.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit in the lab

Open `python_caches.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 7. Check the work by running `python_caches.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
