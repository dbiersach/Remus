# Day 7, Period 2: SAN and the console game

## Learning objectives

By the end of this period, each student pair can:

- Read a move typed in SAN, such as Nf3 or O-O. **Measured by:** The `parse_san` tests pass, and a typo raises `ValueError`.
- Play a whole game in the console. **Measured by:** Two students play `console_game.py` to a finish and the program prints the right result.
- Read commands from `sys.stdin` and answer on stdout. **Measured by:** `python_input_output.py` answers `isready` with `readyok` and stops at `quit`.

## The files

The lab is `python_input_output.py` in the `student` folder, with the answers in `python_input_output_instructor.py` in the `instructor` folder beside it. Open `python_input_output.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `console_game.py`
- `notation.py`

Files that grow this period:

- `test_game.py`

Functions the student pairs write this period:

- `parse_san()` in `notation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

The student pairs fill in the blanks of `python_input_output.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_input_output_instructor.py`.

Parts #1 and #2 pick moves the way the first brains in period 3 do: `random.choice()` takes any item, and a loop that keeps the best piece so far takes the item with the largest value.

Parts #3 and #4 talk the way a UCI engine does. The program reads one command per line from `sys.stdin`, answers `isready` with `readyok`, and sends each answer at once with `flush=True`. Notes for people go to `sys.stderr`, where the GUI does not read them.

### `parse_san()` in `notation.py`

Finds the legal move that matches typed SAN, such as Nf3, by writing the SAN of every legal move and comparing. Matching against real moves means any text Remus accepts is a legal move.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: SAN. The teacher walks through `move_to_san()`, including `Nbd2` and the `+` and `#` endings. |
| 10:45 to 11:05 | Student pairs write `parse_san()`: build the SAN of every legal move and return the one that matches. |
| 11:05 to 11:20 | Student pairs play each other with `console_game.py`, typing moves in SAN. |
| 11:20 to 12:00 | Student pairs work through `python_input_output.py`: `random.choice()`, a loop that keeps the best so far, stderr, and a tiny program that answers `isready` with `readyok`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `notation.py` | `parse_san()` | 90 | 5 | `test_game.py::test_parse_san_finds_each_move` |

Lines to type in all: 5. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## What you edit in the lab

Open `python_input_output.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 16. Check the work by running `python_input_output.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
