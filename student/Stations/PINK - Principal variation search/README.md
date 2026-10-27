# Remus-PINK: Principal variation search

Search the first move with the full window and every other move with a cheap null window first.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `search_later_move()` in `search.py`.

## The changes and why

### `search_later_move()` in `search.py`

Searches a later move with a null window first, which only answers "better or not?", and searches again with the full window only on a surprise. Most later moves are worse, so the cheap question is usually enough.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py PINK`, which plays Remus-PINK against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `search_later_move()` | 393 | 6 | `uv run pytest` |

Lines to type in all: 6. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
