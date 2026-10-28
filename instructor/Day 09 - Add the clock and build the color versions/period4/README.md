# Day 9, Period 4: Color battles

The battles run in `period2/engines`. Each pair copies its own color folder onto a USB stick. On the host laptop, the visitors copy that folder over the folder of the same color in `period2/engines`, and the host opens `play_battle.py` in its own color folder, presses Run Python File, and types the visitor's color. Remus plays two 10-minute games, one with each color, side by side.

## Learning objectives

By the end of this period, each pair can:

- Run a fair match between two color versions. **Measured by:** The pair copies its color folder to another pair's laptop, plays two games against that pair's color, one with each color, and writes the result on the board.
- Read a match result with its margin of error. **Measured by:** `demo_results.py` turns the pair's two battle games, and then its color's league games, into an Elo gap and margin, and the pair says which gap is larger than its margin and why two games cannot show which enhancement is stronger.

## The files

The demo is `demo_results.py` in `student/`, with the answers in `demo_results_instructor.py` in `instructor/`. Open `demo_results.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Each pair works in its own color version folder in `period2/engines`, a complete copy of Remus-WHITE plus one enhancement. Remus-WHITE itself is the `period1` folder.

## The changes and why

The pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each pair puts in its own two battle games, then its color's league games from the teacher's table, and compares the two ranges.
