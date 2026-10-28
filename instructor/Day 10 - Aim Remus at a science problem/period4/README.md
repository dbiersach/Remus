# Day 10, Period 4: Results, tournament, take-home, and wrap-up

The tournament: each pair runs `uv run station_match.py <COLOR>` in the `Stations` folder, two 10-minute games of its color against Remus-WHITE, one with each color, all pairs at once. `uv run estimate_elo.py` measures the Elo rating of Remus against Stockfish. Both add every game to games/remus_games.pgn at the top of the Remus folder.

## Learning objectives

By the end of this period, each pair can:

- Read an experiment's results and their error margins. **Measured by:** `demo_results.py` turns the pair's two tournament games, and then its color's league games, into an Elo gap and margin, and the pair says which gap is larger than its margin.
- Explain one decision your engine made. **Measured by:** Each pair presents one move with its score and principal variation, from Part #3 of `demo_results.py` or its own position, and one powder its phase hunt named.
- Take the code home. **Measured by:** Each student's USB copy opens and runs `uv run pytest`.

## The files

The demo is `demo_results.py` in `student/`, with the answers in `demo_results_instructor.py` in `instructor/`. Both come from `labs/day10/`. Run it with `uv run demo_results.py`.

New files this period:

- `estimate_elo.py`
- `remus.sh`

## The changes and why

The pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each pair puts in its own two tournament games, then its color's league games from the teacher's table, and compares the two ranges.

Part #3 asks `think()` about a back-rank mate and prints each depth's score and principal variation, the line of moves Remus expects. That line is how a pair explains why Remus chose its move.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
