# Day 9, Period 4: Engine battles

The battles run in `engines/student` at the top of the Remus folder. Each student pair copies its finished engine folder from `engines/student` onto a USB stick. On the host laptop, the visitors paste it into the same path, `engines/student`, and replace the folder of the same name. The host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the visitor's engine color, and presses Run Python File. The steps are numbered at the top of `play_battle.py`. Remus plays two 10-minute games, one with each piece color, side by side.

## Learning objectives

By the end of this period, each student pair can:

- Run a fair match between two enhanced engines. **Measured by:** The student pair copies its engine folder to another student pair's laptop, plays two games against that student pair's engine, one with each piece color, and writes the result on the board.
- Read a match result with its margin of error. **Measured by:** `demo_results.py` turns the student pair's two battle games, and then its engine's league games, into an Elo gap and margin, and the student pair says which gap is larger than its margin and why two games cannot show which enhancement is stronger.

## The files

The demo is `demo_results.py` in the `student` folder, with the answers in `demo_results_instructor.py` in the `instructor` folder beside it. Open `demo_results.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Your student pair works in one folder only: your own engine folder in `engines/student`, such as `10 Remus-RED - Transposition table`. That folder already holds the whole Remus engine you finished in period 1, so you add only your one enhancement there. Do not change `00 Remus-WHITE - No enhancements`: it is plain Remus with no enhancement, and it stays as it is so the class can measure every enhancement against it. The `README.md` in each engine folder explains its enhancement, and its section "The code you type" shows every line the student pair types, with line numbers, the lines around it, and how the code works.

## The changes and why

The student pairs fill in the blanks of `demo_results.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_results_instructor.py`.

Parts #1 and #2 of `demo_results.py` turn a match result into a score and an Elo gap, then into a range that holds the true gap 95 times out of 100. When the range includes 0, the match has not shown that the enhancement helped, and more games are needed. Each student pair puts in its own two battle games, then its engine's league games from the designer's table, and compares the two ranges.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: how a battle works. Each student pair copies its finished engine folder, such as `engines/student/10 Remus-RED - Transposition table`, onto its USB stick. The teacher posts the pairings for two rounds; in each round five student pairs host and five visit. |
| 3:10 to 3:40 | Round 1. The visiting student pair pastes its engine folder into the same path on the host laptop, `engines/student`, and replaces the folder of the same name. The host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the visitor's engine color, and presses Run in VS Code. Two 10-minute games run side by side, one with each piece color. Each student pair writes the score on the board. |
| 3:40 to 3:45 | Round 2: the student pairs that visited now host, against new opponents. |
| 3:45 to 4:10 | While the round 2 games run, each student pair turns its round 1 result into an Elo gap with a margin of error in `demo_results.py`, then tries its engine's league games. |
| 4:10 to 4:25 | The class reads the board: which engines won, and why two games prove little. The teacher shows the league table, 110 games for each engine, and compares. |
| 4:25 to 4:30 | Each visiting student pair takes its USB stick back. The visitor's folder stays on the host laptop in place of an engine the host student pair never writes, so the host's own engine folder is untouched. |

## What you edit in the demo

Open `demo_results.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work by running `demo_results.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - Points, Score, and Elo Gap

```python
34 |     # Put your own battle result here, or your color's league games
35 |     wins, draws, losses = 9, 4, 7
36 +     games = wins + draws + losses
37 +     points = wins + draws / 2
38 +     score = points / games
39 +     gap = elo_gap(score)
40 +     print(f"{points} points of {games}: score {score:.2f}, Elo gap {gap:+.0f}")
41 |     print("  (expected 11.0 points of 20: score 0.55, Elo gap +35)")
42 |
```

**How it works:** A win is 1 point and a draw half a point, so 9 wins and 4 draws make 11. The score is points per game, 11 / 20 = 0.55. `elo_gap` turns that score into the rating difference the Elo formula expects, about +35.

### Part #2 - The Margin of Error

```python
43 |     print("Part #2 - The Margin of Error")
44 |     # 95 percent of the time the true score lies within about 2 standard errors
45 +     margin = 1.96 * math.sqrt(score * (1 - score) / games)
46 +     low = elo_gap(score - margin)
47 +     high = elo_gap(score + margin)
48 +     print(f"The Elo gap lies between {low:+.0f} and {high:+.0f}")
49 |     print("  (expected between -121 and +208)")
50 |     # A gap is real when its whole range sits on one side of 0
51 +     if low > 0 or high < 0:
52 +         print("The gap is larger than its margin: the enhancement made a difference")
53 +     else:
54 +         print("The margin reaches past 0: more games are needed to be sure")
55 |
56 |
```

**How it works:** 20 games cannot measure a score exactly. `1.96 * sqrt(score * (1 - score) / games)` is the margin that covers the true score 95 times in 100. Turning the low and high scores into Elo gives a range. If the whole range is above 0 or below 0, the enhancement really changed the strength; if it reaches past 0, more games are needed.
