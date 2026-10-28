# python_modules.py: One file uses another

*Day 4, period 1. The lab file is `student/Day 04 - Keep only legal moves/period1/python_modules.py`, and the answers are in `instructor/Day 04 - Keep only legal moves/period1/python_modules_instructor.py`.*

## The big picture

Remus is many files, and each one does one job. A file uses another with `import`
instead of copying its code. This lab imports four Remus files, finds the knight moves
from g1 with their functions, and shows why an imported file prints nothing.

## Where this piece fits

The lab sits in the Day 4, period 1 folder, beside the Remus code from Day 3, so its
imports find `board.py`, `game_state.py`, `move_generation.py`, and `moves.py`. Every
later Remus file starts with imports like these.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`move_generation.py`](move_generation.md), [`moves.py`](moves.md)
- **Used by:** nothing; it is practice for every Remus file

## Words to know

- **module:** a Python file that other files import.
- **import:** runs another file once and hands over its names, such as `new_board`.
- **__name__:** `"__main__"` in the file that `uv run` starts, and the file's own name when it is imported.
- **git branch:** a separate line of commits, so an experiment never breaks the class code.

## How it works

1. Type the four import lines at the top of the file.
2. Part #1: print `__name__` for this file and for `board.py`.
3. Part #2: build the start board and list the knight moves from g1.
4. Parts #3 and #4 happen in the terminal: run `board.py` on its own, then make a branch, a commit, and read the log.

The pair types 11 lines.

## Try it

From inside `student/Day 04 - Keep only legal moves/period1`, run:

```bash
uv run python_modules.py
```

You should see: `__main__`, then `board`, then the knight moves g1f3 and g1h3, then the commands for the terminal.

## Puzzle questions

1. Why would Lucas Chess break if `board.py` printed its board every time another file imported it?
2. Where does Python look for `board.py` when the lab says `import board`?
