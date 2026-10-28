# Remus-PURPLE: Pawn structure

Penalize doubled and isolated pawns and reward passed pawns.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Run a fair experiment against Remus-WHITE: same opening, both colors. **Measured by:** In the Day 10 tournament, `uv run station_match.py <COLOR>` plays both 10-minute games with no illegal moves or crashes, and the pair says why two games cannot show whether the enhancement helps.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `pawn_structure()` in `evaluation.py`.

## The changes and why

### `pawn_structure()` in `evaluation.py`

Counts doubled and isolated pawns as weaknesses and passed pawns as strengths, more the further they have gone. Pawns cannot move back, so their shape lasts the whole game.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py PURPLE`, which plays Remus-PURPLE against Remus-WHITE and adds every game to games/remus_games.pgn.
