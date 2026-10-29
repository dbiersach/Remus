# Remus-CYAN: Mating bonus

With a big material lead, drive the losing king to the edge and bring the winning king close.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

White has king and rook, Black has only a king. Mate needs the Black king on the edge, and it takes far more than 4 plies of good moves to drive it there. Remus-WHITE sees no mate within its depth and scores every rook move the same, +500, so it shuffles. Remus-CYAN adds a bonus once one side leads by at least 200 and the losing side has at most 600 left: 10 points for each step the losing king stands from the center, and 4 points for each step the winning king has closed in. Now every move that squeezes the king toward the edge scores higher, and the search walks it into a mating net.

## Why it makes Remus stronger

An evaluation term can stand in for a search that is too deep to run. The bonus turns a long plan, "push the king to the edge, then mate", into small steps that a shallow search can see.

## What it costs

One scan of the board to count material and find the kings, in every evaluated position. In most positions the margins are not met and the bonus is 0, so the cost is the scan only.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-CYAN | 425,602 | 99% | 4,864 | 3.1 |

## What to expect

Faster wins in won endgames, and no change before that. Many games are decided or drawn before such an endgame appears, so the league rating moves little.

## Where your code fits

`white_score()` in `evaluation.py` adds `mating_bonus(board)` to material and placement. `CENTER_DISTANCE` gives each row and column's distance from the center: 3 on the edge, 0 in the middle.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `mating_bonus()` in `evaluation.py`.

## The changes and why

### `mating_bonus()` in `evaluation.py`

With a big lead and a weak opponent, rewards pushing the losing king to the edge and bringing the winning king close. Without it, Remus can be a queen up and still wander without mating.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-CYAN plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-CYAN plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the folder above this one.
