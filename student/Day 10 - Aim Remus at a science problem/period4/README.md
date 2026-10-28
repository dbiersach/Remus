# Day 10, Period 4: Results, tournament, take-home, and wrap-up

The tournament: each pair opens `play_tournament.py` in its version folder under `Remus` and presses Run in VS Code: two 10-minute games of its color against Remus-WHITE, one with each color, all pairs at once. Running `estimate_elo.py` in the GOLD folder measures the Elo rating of Remus-GOLD against Stockfish. Both add every game to games/remus_games.pgn at the top of the repository.

## Learning objectives

By the end of this period, each pair can:

- Read an experiment's results and their error margins. **Measured by:** `demo_results.py` turns the pair's two tournament games, and then its color's league games, into an Elo gap and margin, and the pair says which gap is larger than its margin.
- Explain one decision your engine made. **Measured by:** Each pair presents one move from its tournament games with the score and principal variation that Lucas Chess shows for Remus-GOLD, and one powder its phase hunt named.
- Take the code home. **Measured by:** Each student's USB copy opens and runs `uv run pytest`.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the `Remus/11 GOLD - All enhancements` folder beside the Day folders. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

The demo is `demo_results.py` in `student/`, with the answers in `demo_results_instructor.py` in `instructor/`. Open `demo_results.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each pair puts in its own two tournament games, then its color's league games from the teacher's table, and compares the two ranges.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `hidden_peak.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit in the demo

Open `demo_results.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work by running `demo_results.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
