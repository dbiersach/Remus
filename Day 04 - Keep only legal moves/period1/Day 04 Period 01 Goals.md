# Day 4, Period 1: Python lab 6: modules, imports, __main__, git

## Learning objectives

By the end of this period, each pair can:

- Split code into modules and import one from another. **Measured by:** The lab's two files run together, and `uv run` on the imported file alone prints its own self-check only through `main()`.
- Save work with git: switch to a branch, commit, and read the log. **Measured by:** `git log --oneline` shows the pair's commit on its own branch.

## The files

The lab is `python_modules.py` in the `student` folder, with the answers in `python_modules_instructor.py` in the `instructor` folder beside it. Open `python_modules.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_modules.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_modules_instructor.py`.

The lab imports `board.py`, `game_state.py`, `move_generation.py`, and `moves.py` from the same folder. An import runs the other file once and hands over its functions, so no code is copied.

Part #1 prints `__name__`: the file that VS Code runs is `__main__`, and an imported file keeps its own name. That is why `board.py` prints its board when VS Code runs `board.py` and stays silent when the lab imports it, and why every Remus print sits inside `main()`.

Part #2 calls `new_board()` and `knight_moves()` from the imported files and lists the two knight moves from g1. Part #3 runs `board.py` on its own in VS Code, and Part #4 makes a git branch, a commit, and the log in the terminal.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a module is a file, `import` reads it, and `if __name__ == "__main__"` keeps a file quiet when another file imports it. |
| 8:45 to 9:20 | Pairs work through Parts #1 to #3 of `python_modules.py`: every file has a `__name__`, use yesterday's `board.py` and `move_generation.py`, and list the knight moves from g1. |
| 9:20 to 9:30 | Slides: git. The teacher shows `fetch`, `switch -c`, `commit`, and `log` on the projector. |
| 9:30 to 9:50 | Pairs finish Part #4 and save the lab with their first commit. |
| 9:50 to 10:00 | Every pair shows its `git log` to the teacher or the assistant. |

## What you edit in the lab

Open `python_modules.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 11. Check the work by running `python_modules.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
