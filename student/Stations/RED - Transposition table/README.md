# Remus-RED: Transposition table

Remember positions already searched, so the same position reached in two move orders is scored once.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `store()` in `transposition_table.py`, `probe()` in `transposition_table.py`, `test_transposition_table_bounds()` in `test_upgrades.py`.

## The changes and why

### `store()` in `transposition_table.py`

Saves what one search learned about a position under its key: the depth, the score, whether that score is exact or only a bound, and the best move. A dict holds the table, so looking a position up again costs one step.

### `probe()` in `transposition_table.py`

Looks up a position in the table and returns a stored score only when it answers this search: it was searched deep enough, and its bound fits the window. One position reached by two move orders is then searched once.

### `test_transposition_table_bounds()` in `test_upgrades.py`

Proves the rules of `probe()` with three made-up entries before any real search uses them. A bound is the tricky part: "at least 80" settles a window whose beta is 70, but says nothing useful when beta is 100.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py RED`, which plays Remus-RED against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `transposition_table.py` | `store()` | 25 | 3 | `test_upgrades.py::test_transposition_table_bounds` |
| `transposition_table.py` | `probe()` | 34 | 11 | `test_upgrades.py::test_transposition_table_bounds` |
| `test_upgrades.py` | `test_transposition_table_bounds()` | 17 | 13 | `uv run pytest` |

Lines to type in all: 27. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
