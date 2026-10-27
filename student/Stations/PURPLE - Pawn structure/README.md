# Remus-PURPLE: Pawn structure

Penalize doubled and isolated pawns and reward passed pawns.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `pawn_structure()` in `evaluation.py`.

## The changes and why

### `pawn_structure()` in `evaluation.py`

Counts doubled and isolated pawns as weaknesses and passed pawns as strengths, more the further they have gone. Pawns cannot move back, so their shape lasts the whole game.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py PURPLE`, which plays Remus-PURPLE against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `evaluation.py` | `pawn_structure()` | 146 | 29 | `test_upgrades.py::test_pawn_structure_is_level_at_the_start`, `test_upgrades.py::test_doubled_isolated_pawns_cost_points`, `test_upgrades.py::test_a_passed_pawn_earns_a_bonus` |

Lines to type in all: 29. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
