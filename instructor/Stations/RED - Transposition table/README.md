# Remus-RED: Transposition table

Remember positions already searched, so the same position reached in two move orders is scored once.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `probe()` in `transposition_table.py`.

## The changes and why

### `probe()` in `transposition_table.py`

Looks up a position in the table and returns a stored score only when it answers this search: it was searched deep enough, and its bound fits the window. One position reached by two move orders is then searched once.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py RED`, which plays Remus-RED against Remus-WHITE and adds every game to games/remus_games.pgn.
