# Day 5, Period 2: Castling

## Learning objectives

By the end of this period, each pair can:

- State the castling rules: no earlier king or rook move, empty squares between, and no check on the king's path. **Measured by:** Six-position quiz on castling: each pair gets at least five right.
- Update the castling rights after any move. **Measured by:** The castling tests in `test_special_moves.py` pass, including a captured rook.

## The files

New files this period:

- `test_special_moves.py`

Files that grow this period:

- `legal_moves.py`
- `make_move.py`

Functions the pairs write this period:

- `update_castling_rights()` in `make_move.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `update_castling_rights()` in `make_move.py`

Removes castling rights when a king or rook leaves its square, or when a rook is captured on its square. Rights only ever disappear, so `replace()` deletes letters from a string such as "KQkq".

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Chess refresher on the demonstration board: the five castling conditions. The rook may cross an attacked square (b1), and a rook captured on its home square removes that right. |
| 10:45 to 11:00 | Slides: the teacher's castling generation and the attacked-square checks. |
| 11:00 to 11:20 | Pairs write `update_castling_rights()`, the table of which moves remove K, Q, k, or q. |
| 11:20 to 11:50 | Pairs run the castling tests and build one castling position of their own to test. |
| 11:50 to 12:00 | Show and choose for `update_castling_rights()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `update_castling_rights()` | 24 | 4 | `test_special_moves.py::test_rook_capture_removes_the_right` |

Lines to type in all: 4. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
