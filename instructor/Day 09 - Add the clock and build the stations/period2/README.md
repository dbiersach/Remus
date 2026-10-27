# Day 9, Period 2: Python lab 12 and the enhancement stations

Each pair builds one color station in the `Stations` folder, such as `RED - Transposition table`. The code in this Day folder is Remus-WHITE, the starting point of every station.

## Learning objectives

By the end of this period, each pair can:

- Use a dict as a cache with tuples as keys. **Measured by:** The lab remembers perft counts already computed and prints the time saved.
- Add one enhancement to Remus-WHITE. **Measured by:** The station's own tests pass in its folder.

## The files

The lab is `python_caches.py` in `student/`, with the answers in `python_caches_instructor.py` in `instructor/`. Both come from `labs/day09/`. Run it with `uv run python_caches.py`.

The Remus code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_caches.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_caches_instructor.py`.

Part #1: `remembered_perft()` stores each answer in a dict under the tuple key `(name, depth)`. The second call finds the answer and returns at once. The RED station's transposition table remembers search results the same way.

Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 to g7, which the CYAN station needs, and `random.seed()`, which makes a random choice repeat on every run.

Part #4 is a teacher demo with no blanks: one thread counts until another sets a `threading.Event`. `think()` stops the same way when the GUI sends `stop`.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
