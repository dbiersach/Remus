# Day 10, Period 4: Results, tournament, take-home, and wrap-up

`uv run tournament.py` plays the class round robin, and `uv run estimate_elo.py` measures the Elo rating of Remus against Stockfish. Both add every game to games/remus_games.pgn at the top of the Remus folder.

## Learning objectives

By the end of this period, each pair can:

- Read an experiment's results and their error margins. **Measured by:** Each pair says whether its color's Elo gap is larger than its margin.
- Explain one decision your engine made. **Measured by:** Each pair presents one move with its score and principal variation, and one choice its beam time agent made.
- Take the code home. **Measured by:** Each student's USB copy opens and runs `uv run pytest`.

## The files

New files this period:

- `estimate_elo.py`
- `remus.sh`
- `tournament.py`

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
