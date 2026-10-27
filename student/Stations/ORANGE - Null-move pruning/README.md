# Remus-ORANGE: Null-move pruning

Pass the turn in a shallow search: if passing still wins, a real move will too, so stop early.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `make_null_move()` in `search.py`, `undo_null_move()` in `search.py`.

## The changes and why

### `make_null_move()` in `search.py`

Passes the turn without moving a piece, and returns the en passant target so it can be put back. If the position is still winning after a free move for the opponent, a real move will be too, so the search can stop early.

### `undo_null_move()` in `search.py`

Takes the pass back: removes its history entry, gives the turn back, and restores the en passant target. Like every undo in Remus, it must restore the state exactly.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py ORANGE`, which plays Remus-ORANGE against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `make_null_move()` | 395 | 5 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |
| `search.py` | `undo_null_move()` | 415 | 3 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |

Lines to type in all: 8. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
