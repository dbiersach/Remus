# Day 2, Period 4: make_move.py: make and undo ordinary moves

## Learning objectives

By the end of this period, each pair can:

- Make a move and take it back exactly. **Measured by:** The make and undo tests pass, and ten moves made and undone leave the same state as the start, clocks and rights included.
- Explain why undo needs a record of what the move changed. **Measured by:** The pair names what a capture destroys (the captured piece) and where the undo record keeps it.

## The files

New files this period:

- `make_move.py`

Files that grow this period:

- `test_make_move.py`

Functions the pairs write this period:

- `make_move()` in `make_move.py`
- `undo_move()` in `make_move.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `make_move()` in `make_move.py`

Moves a piece and empties the square it left, then updates the clocks and gives the turn to the other side. Before changing anything, it writes down every value the move will destroy, such as the captured piece and the old clocks, in an undo record. That record is the only way to take the move back, and a search in Remus makes and undoes thousands of moves for every move it plays.

### `undo_move()` in `make_move.py`

Puts back everything a move changed, using the undo record that `make_move()` saved: the moved piece, the captured piece, the side to move, and the clocks and rights. The search will make and undo millions of moves, so undo must restore the position exactly, or Remus slowly corrupts its own board.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `make_move()` | 13 | 23 | `test_make_move.py::test_e2e4_changes_board_and_turn`, `test_make_move.py::test_knight_move_counts_toward_fifty_moves`, `test_make_move.py::test_capture_and_undo`, `test_make_move.py::test_ten_moves_made_and_undone_return_the_start` |
| `make_move.py` | `undo_move()` | 35 | 9 | `test_make_move.py::test_capture_and_undo`, `test_make_move.py::test_ten_moves_made_and_undone_return_the_start` |

Lines to type in all: 32. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
