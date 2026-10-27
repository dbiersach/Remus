# Remus-BROWN: Late move reductions

Search late, quiet moves one ply shallower, and in full only if they surprise.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `reduction()` in `search.py`.

## The changes and why

### `reduction()` in `search.py`

Returns 1 for a late, quiet move that gives no check at depth 3 or more, and 0 otherwise. Late moves in a well-ordered list are rarely best, so a shallower look saves time, and a surprise earns a full search.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py BROWN`, which plays Remus-BROWN against Remus-WHITE and adds every game to games/remus_games.pgn.
