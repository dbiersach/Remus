# Remus-CYAN: Mating bonus

With a big material lead, drive the losing king to the edge and bring the winning king close.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `mating_bonus()` in `evaluation.py`.

## The changes and why

### `mating_bonus()` in `evaluation.py`

With a big lead and a weak opponent, rewards pushing the losing king to the edge and bringing the winning king close. Without it, Remus can be a queen up and still wander without mating.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py CYAN`, which plays Remus-CYAN against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `evaluation.py` | `mating_bonus()` | 144 | 24 | `test_upgrades.py::test_mating_bonus_prefers_the_losing_king_in_the_corner` |

Lines to type in all: 24. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
