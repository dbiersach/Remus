# Day 7, Period 2: SAN and the console game

## Learning objectives

By the end of this period, each pair can:

- Read a move typed in SAN, such as Nf3 or O-O. **Measured by:** The `parse_san` tests pass, and a typo raises `ValueError`.
- Play a whole game in the console. **Measured by:** Two students play `console_game.py` to a finish and the program prints the right result.

## The files

New files this period:

- `console_game.py`
- `notation.py`

Files that grow this period:

- `test_game.py`

Functions the pairs write this period:

- `parse_san()` in `notation.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `parse_san()` in `notation.py`

Finds the legal move that matches typed SAN, such as Nf3, by writing the SAN of every legal move and comparing. Matching against real moves means any text Remus accepts is a legal move.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `notation.py` | `parse_san()` | 86 | 5 | `test_game.py::test_parse_san_finds_each_move` |

Lines to type in all: 5. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
