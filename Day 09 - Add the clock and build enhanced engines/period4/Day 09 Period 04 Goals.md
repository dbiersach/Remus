# Day 9, Period 4: Color battles

The battles run in `engines/student` at the top of the Remus folder. Each student pair copies its finished engine folder from `engines/student` onto a USB stick. On the host laptop, the visitors paste it into the same path, `engines/student`, and replace the folder of the same name. The host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the visitor's engine color, and presses Run Python File. The steps are numbered at the top of `play_battle.py`. Remus plays two 10-minute games, one with each piece color, side by side.

## Learning objectives

By the end of this period, each student pair can:

- Run a fair match between two color versions. **Measured by:** The student pair copies its engine folder to another student pair's laptop, plays two games against that student pair's engine color, one with each piece color, and writes the result on the board.
- Read a match result with its margin of error. **Measured by:** `demo_results.py` turns the student pair's two battle games, and then its engine color's league games, into an Elo gap and margin, and the student pair says which gap is larger than its margin and why two games cannot show which enhancement is stronger.

## The files

The demo is `demo_results.py` in the `student` folder, with the answers in `demo_results_instructor.py` in the `instructor` folder beside it. Open `demo_results.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Each student pair works in its own engine folder in `engines/student`, a complete copy of Remus-WHITE plus one enhancement. Remus-WHITE itself is in the `period1` folder.

## The changes and why

The student pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each student pair puts in its own two battle games, then its engine color's league games from the designer's table, and compares the two ranges.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: how a battle works. Each student pair copies its finished engine folder, such as `engines/student/10 RED - Transposition table`, onto its USB stick. The teacher posts the pairings for two rounds; in each round five student pairs host and five visit. |
| 3:10 to 3:40 | Round 1. The visiting student pair pastes its engine folder into the same path on the host laptop, `engines/student`, and replaces the folder of the same name. The host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the visitor's engine color, and presses Run in VS Code. Two 10-minute games run side by side, one with each piece color. Each student pair writes the score on the board. |
| 3:40 to 3:45 | Round 2: the student pairs that visited now host, against new opponents. |
| 3:45 to 4:10 | While the round 2 games run, each student pair turns its round 1 result into an Elo gap with a margin of error in `demo_results.py`, then tries its engine color's league games. |
| 4:10 to 4:25 | The class reads the board: which engine colors won, and why two games prove little. The teacher shows the league table, 110 games for each engine color, and compares. |
| 4:25 to 4:30 | Each visiting student pair takes its USB stick back. The visitor's folder stays on the host laptop in place of an engine color the host student pair never writes, so the host's own engine folder is untouched. |

## What you edit in the demo

Open `demo_results.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work by running `demo_results.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
