# Remus-BLUE: Killer moves

Try quiet moves that caused a cutoff at the same depth right after the captures.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `remember_killer()` in `search.py`.

## The changes and why

### `remember_killer()` in `search.py`

Keeps up to two quiet moves per ply that caused a cutoff. A move that refuted one position often refutes its neighbors, so trying it early saves work.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py BLUE`, which plays Remus-BLUE against Remus-WHITE and adds every game to games/remus_games.pgn.
