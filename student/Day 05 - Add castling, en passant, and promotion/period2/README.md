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

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `update_castling_rights()` in `make_move.py`

Removes castling rights when a king or rook leaves its square, or when a rook is captured on its square. Rights only ever disappear, so `replace()` deletes letters from a string such as "KQkq".

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `update_castling_rights()` | 24 | 4 | `test_special_moves.py::test_rook_capture_removes_the_right` |

Lines to type in all: 4. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
