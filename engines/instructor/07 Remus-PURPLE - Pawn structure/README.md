# Remus-PURPLE: Pawn structure

Penalize doubled and isolated pawns and reward passed pawns.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

White pawns on c2, c3, and e4, Black pawns on d6 and e5: White's c-pawns are doubled (two on one file), and the e4 pawn is isolated (no White pawn on the d- or f-file beside it).

![White pawns on c2, c3, and e4 against Black pawns on d6 and e5](../../../misc/docs/images/boards/purple_pawns.svg)

*The yellow squares are White's doubled pawns on the c-file. The red square is the isolated pawn on e4: no White pawn stands anywhere on the d-file or the f-file to protect it.*

Remus-PURPLE scores each doubled pawn -8 and each isolated pawn -20. A passed pawn, with no enemy pawn in front of it on its own file or a neighboring file, earns a bonus that grows as it advances: 0, 10, 20, 40, 60, and then 70 one step from promotion. Remus-WHITE counts every pawn as 100 plus its square's placement value and sees none of this.

## Why it makes Remus stronger

Pawns cannot move backward, so a weak pawn stays weak for the whole game, and a passed pawn becomes a queen threat that ties down enemy pieces. A search at depth 4 cannot see those long-term effects, but an evaluation term can score them in every position.

## What it costs

`pawn_structure()` scans the board for pawns, then looks ahead of each pawn for enemy pawns, in every evaluated position. Evaluation is most of Remus's work at the ends of lines, so Remus-PURPLE evaluates fewer positions a second than Remus-WHITE. The number of positions per depth changes a little either way, because different scores lead alpha-beta to different cutoffs.

## Measured against Remus-WHITE

Each version searched the ten positions of the designer's benchmark, `misc/scripts/remus_benchmark.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-PURPLE | 452,398 | 105% | 4,547 | 3.1 |

## What to expect

Better pawn moves: Remus-PURPLE avoids doubling its own pawns, attacks isolated enemy pawns, and pushes passed pawns in the endgame. The cost in speed can cancel the gain at a short clock.

## Where your code fits

`white_score()` in `evaluation.py` adds `pawn_structure(board)` to material and placement, and `explain_evaluation()` prints it as its own line, so a student pair can see the term in any position.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 Remus-WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `pawn_structure()` in `evaluation.py`.

## The changes and why

### `pawn_structure()` in `evaluation.py`

Counts doubled and isolated pawns as weaknesses and passed pawns as strengths, more the further they have gone. Pawns cannot move back, so their shape lasts the whole game.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `basic_test.py` in VS Code and press Run: Remus-PURPLE plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-PURPLE plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `misc/scripts/version_match.py`, which plays the games.
