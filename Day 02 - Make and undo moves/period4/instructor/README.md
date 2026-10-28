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

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `make_move()` in `make_move.py`

Moves a piece and empties the square it left, then updates the clocks and gives the turn to the other side. Before changing anything, it writes down every value the move will destroy, such as the captured piece and the old clocks, in an undo record. That record is the only way to take the move back, and a search in Remus makes and undoes thousands of moves for every move it plays.

### `undo_move()` in `make_move.py`

Puts back everything a move changed, using the undo record that `make_move()` saved: the moved piece, the captured piece, the side to move, and the clocks and rights. The search will make and undo millions of moves, so undo must restore the position exactly, or Remus slowly corrupts its own board.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
