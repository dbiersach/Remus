# Remus-BLUE: Killer moves

Try quiet moves that caused a cutoff at the same depth right after the captures.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `remember_killer()` in `search.py`, `order_moves()` in `move_ordering.py`, `test_killers_keep_two_quiet_moves()` in `test_upgrades.py`.

## The changes and why

### `remember_killer()` in `search.py`

Keeps up to two quiet moves per ply that caused a cutoff. A move that refuted one position often refutes its neighbors, so trying it early saves work.

### `order_moves()` in `move_ordering.py`

Sorts the moves so captures come first by MVV-LVA, then this ply's killer moves, then every other move. The earlier a good move comes, the sooner alpha-beta cuts off the rest.

### `test_killers_keep_two_quiet_moves()` in `test_upgrades.py`

Feeds three cutoff moves to `remember_killer()` and checks that only the two newest stay, newest first. Writing the expected list before running the test is how a pair shows it understands the two slots.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py BLUE`, which plays Remus-BLUE against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `remember_killer()` | 394 | 6 | `test_upgrades.py::test_killers_keep_two_quiet_moves` |
| `move_ordering.py` | `order_moves()` | 53 | 11 | `test_search.py::test_capture_moves_and_mvv_lva` |
| `test_upgrades.py` | `test_killers_keep_two_quiet_moves()` | 21 | 5 | `uv run pytest` |

Lines to type in all: 22. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
