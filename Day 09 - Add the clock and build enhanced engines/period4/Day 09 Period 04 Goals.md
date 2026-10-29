# Day 9, Period 4: Color battles

The battles run in `period2/student/engines`. Each pair copies its own color folder onto a USB stick. On the host laptop, the visitors copy that folder over the folder of the same color in `period2/student/engines`, and the host opens `play_battle.py` in its own color folder, presses Run Python File, and types the visitor's color. Remus plays two 10-minute games, one with each color, side by side.

## Learning objectives

By the end of this period, each pair can:

- Run a fair match between two color versions. **Measured by:** The pair copies its color folder to another pair's laptop, plays two games against that pair's color, one with each color, and writes the result on the board.
- Read a match result with its margin of error. **Measured by:** `demo_results.py` turns the pair's two battle games, and then its color's league games, into an Elo gap and margin, and the pair says which gap is larger than its margin and why two games cannot show which enhancement is stronger.

## The files

The demo is `demo_results.py` in the `student` folder, with the answers in `demo_results_instructor.py` in the `instructor` folder beside it. Open `demo_results.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Each pair works in its own color version folder in `period2/student/engines`, a complete copy of Remus-WHITE plus one enhancement. Remus-WHITE itself is in the `period1` folder.

## The changes and why

The pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each pair puts in its own two battle games, then its color's league games from the teacher's table, and compares the two ranges.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: how a battle works. Each pair copies its own color folder from `period2/student/engines` onto its USB stick. The teacher posts the pairings for two rounds; in each round five pairs host and five visit. |
| 3:10 to 3:40 | Round 1. The visiting pair copies its color folder over the folder of the same color in the host laptop's `engines` folder. The host opens `play_battle.py` in its own color folder, presses Run in VS Code, and types the visitor's color. Two 10-minute games run side by side, one with each color. Each pair writes the score on the board. |
| 3:40 to 3:45 | Round 2: the pairs that visited now host, against new opponents. |
| 3:45 to 4:10 | While the round 2 games run, each pair turns its round 1 result into an Elo gap with a margin of error in `demo_results.py`, then tries its color's league games. |
| 4:10 to 4:25 | The class reads the board: which colors won, and why two games prove little. The teacher shows the league table, 110 games for each color, and compares. |
| 4:25 to 4:30 | Each host restores the visitor's folder with `git restore` so its own repository holds only its own color. |

## What you edit in the demo

Open `demo_results.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work by running `demo_results.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
