# Day 7, Period 2: SAN and the console game

## Learning objectives

By the end of this period, each pair can:

- Read a move typed in SAN, such as Nf3 or O-O. **Measured by:** The `parse_san` tests pass, and a typo raises `ValueError`.
- Play a whole game in the console. **Measured by:** Two students play `console_game.py` to a finish and the program prints the right result.
- Read commands from `sys.stdin` and answer on stdout. **Measured by:** `python_input_output.py` answers `isready` with `readyok` and stops at `quit`.

## The files

The lab is `python_input_output.py` in `student/`, with the answers in `python_input_output_instructor.py` in `instructor/`. Both come from `labs/day07/`. Run it with `uv run python_input_output.py`.

New files this period:

- `console_game.py`
- `notation.py`

Files that grow this period:

- `test_game.py`

Functions the pairs write this period:

- `parse_san()` in `notation.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

The pairs fill in the blanks of `python_input_output.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_input_output_instructor.py`.

Parts #1 and #2 pick moves the way the first brains in period 3 do: `random.choice()` takes any item, and `max(..., key=victim_value)` takes the item with the largest value.

Parts #3 and #4 talk the way a UCI engine does. The program reads one command per line from `sys.stdin`, answers `isready` with `readyok`, and sends each answer at once with `flush=True`. Notes for people go to `sys.stderr`, where the GUI does not read them.

### `parse_san()` in `notation.py`

Finds the legal move that matches typed SAN, such as Nf3, by writing the SAN of every legal move and comparing. Matching against real moves means any text Remus accepts is a legal move.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
