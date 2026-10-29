# demo_results.py: Read a battle result

*Day 9, period 4. The demo file is `Day 09 - Add the clock and build enhanced engines/period4/student/demo_results.py`, and the answers are in `Day 09 - Add the clock and build enhanced engines/period4/instructor/demo_results_instructor.py`.*

## The big picture

A match ends with a score, but luck plays a part, and luck plays a larger part the
fewer games there are. This demo turns wins, draws, and losses into an Elo gap and a
margin of error, and says whether the result shows a real difference. A student pair puts in
its two battle games first, then its engine color's games from the designer's league,
and sees the margin shrink as the games add up.

## Where this piece fits

The demo runs in the Day 9, period 4 folder, during the second round of battles, and uses only Python's `math` module.
`estimate_elo.py` and `version_league.py` fit ratings with the same Elo formula.

- **Uses:** nothing from Remus
- **Used by:** nothing; each student pair uses it to read its battle and its engine color's league result

## Words to know

- **score:** points per game: a win is 1, a draw one half, a loss 0.
- **Elo gap:** the rating difference that the Elo formula expects for a score. A score of 0.55 is a gap of about 35.
- **margin of error:** how far the true value may lie from the measured one, 95 times out of 100.

## How it works

1. Part #1: count the games and points, and turn the score into an Elo gap.
2. Part #2: work out the margin, the lowest and highest gap it allows, and whether the range includes 0.

The student pair types 13 lines.

## Try it

Open `demo_results.py` in `Day 09 - Add the clock and build enhanced engines/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 11.0 points of 20, a gap of +35 between -121 and +208, and "more games are needed".

## Puzzle questions

1. How many games would make the margin half as wide?
2. Put your own engine color's result into Part #1. Is your enhancement's gap larger than its margin?
