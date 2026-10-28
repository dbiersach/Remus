# Remus-GRAY: King safety

While the enemy queen is on the board, reward pawns that shelter the king.

## Learning objectives

By the end of Day 9, each pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the version folder.
- Run a fair experiment against Remus-WHITE: same opening, both colors. **Measured by:** In the Day 10 tournament, `play_tournament.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the pair presses Run in VS Code, and the pair says why two games cannot show whether the enhancement helps.

## The idea, with an example

White has castled kingside: king on g1, pawns on f2, g2, and h2. Each of the king's three files has a White pawn one or two squares in front, so Remus-GRAY adds 3 x 15 = 45 points. Push the h-pawn to h4, and the h-file no longer shelters the king: 30 points. The bonus counts only while the enemy queen is on the board, because the queen is the piece that makes an open king dangerous. Once the queens come off, the king should walk toward the center, and the term is 0.

## Why it makes Remus stronger

A king attack takes many moves to build, too many for a depth 4 search to see. The shield bonus teaches Remus to castle and to keep the pawns in front of its king, before an attack is in range of the search.

## What it costs

A scan of the board for the enemy queen and the king, and up to six squares checked in front of the king, in every evaluated position. Remus-GRAY evaluates a few positions a second fewer than Remus-WHITE.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-GRAY | 459,732 | 107% | 4,927 | 3.1 |

## What to expect

Earlier castling, fewer pawn pushes in front of its own king, and a reason to trade queens when its own shield is broken.

## Where your code fits

`white_score()` in `evaluation.py` adds `king_safety(board)` to material and placement. White's pawns stand in front of its king at smaller rows, because row 0 is rank 8, so the code steps the other way for Black.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `king_safety()` in `evaluation.py`.

## The changes and why

### `king_safety()` in `evaluation.py`

Rewards each pawn that shelters the king on its own file or a neighbor, one or two squares ahead, while the enemy queen is on the board. A king without pawn cover is easy to attack.

## Check it

Check the work from inside this folder with `uv run pytest`. Then open `smoke_test.py` in VS Code and press Run: Remus-GRAY plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, copy the visiting pair's color folder into the `Remus` folder, open `play_battle.py`, press Run, and type the visitor's color: Remus-GRAY plays it twice at 10 minutes a side, once with each color. In the Day 10 tournament, open `play_tournament.py` and press Run: Remus-GRAY plays Remus-WHITE twice, once with each color, at 10 minutes a side, and both games go into games/remus_games.pgn. Each script runs `version_match.py` from the `Remus` folder above this one.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `evaluation.py` | `king_safety()` | 126 | 24 | `test_upgrades.py::test_king_safety_rewards_the_pawn_shield` |

Lines to type in all: 24. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
