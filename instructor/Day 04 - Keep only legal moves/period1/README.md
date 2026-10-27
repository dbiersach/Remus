# Day 4, Period 1: Python lab 6: modules, imports, __main__, git

## Learning objectives

By the end of this period, each pair can:

- Split code into modules and import one from another. **Measured by:** The lab's two files run together, and `uv run` on the imported file alone prints its own self-check only through `main()`.
- Save work with git: switch to a branch, commit, and read the log. **Measured by:** `git log --oneline` shows the pair's commit on its own branch.

## The files

The lab is `python_modules.py` in `student/`, with the answers in `python_modules_instructor.py` in `instructor/`. Both come from `labs/day04/`. Run it with `uv run python_modules.py`.

The Remus code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_modules.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_modules_instructor.py`.

The lab imports `board.py`, `game_state.py`, `move_generation.py`, and `moves.py` from the same folder. An import runs the other file once and hands over its functions, so no code is copied.

Part #1 prints `__name__`: the file that `uv run` starts is `__main__`, and an imported file keeps its own name. That is why `board.py` prints its board under `uv run board.py` and stays silent when the lab imports it, and why every Remus print sits inside `main()`.

Part #2 calls `new_board()` and `knight_moves()` from the imported files and lists the two knight moves from g1. Parts #3 and #4 run in the terminal: `uv run board.py` on its own, then a git branch, a commit, and the log.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
