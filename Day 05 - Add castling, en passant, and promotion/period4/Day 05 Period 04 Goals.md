# Day 5, Period 4: Promotion, and Remus plays in Lucas Chess

Register `remus.bat` from the `student` folder as an engine in Lucas Chess and play your own Remus. It plays random legal moves, and every special move works.

## Learning objectives

By the end of this period, each student pair can:

- Promote a pawn to any of four pieces. **Measured by:** The promotion tests pass for queen, rook, bishop, and knight.
- Explain why a player sometimes promotes to a knight. **Measured by:** Running `demo_promotion.py` prints stalemate for b8=Q, b8=R, and b8=B and checkmate for b8=N, and the student pair says why the queen only draws.
- Play Remus in Lucas Chess. **Measured by:** The student pair registers `remus.bat`, plays one game, and sees a random legal reply to every move, special moves included.

## The files

The demo is `demo_promotion.py` in the `student` folder, with the answers in `demo_promotion_instructor.py` in the `instructor` folder beside it. Open `demo_promotion.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `remus.bat`
- `uci_engine.py`

Files that grow this period:

- `make_move.py`
- `test_special_moves.py`

## The changes and why

The student pairs fill in the blanks of `demo_promotion.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_promotion_instructor.py`.

`demo_promotion.py` sets up a puzzle: White's pawn on b7 promotes on b8 next to the Black king on a6. The student pair writes the loop that tries all four promotion pieces, counts Black's legal replies, and names the result.

![White king c6, bishop b6, and pawn b7 against the Black king on a6](../../misc/docs/images/boards/promotion_puzzle.svg)

*The puzzle: White's king on c6, bishop on b6, and pawn on b7 against Black's king on a6. The pawn promotes on b8 (the green arrow).*

With no legal reply, `in_check()` decides between checkmate and stalemate. A queen, a rook, or a bishop takes away every square without giving check, so the game is a draw; only the knight on b8 gives check, and the king has nowhere to go. Every promotion is undone, and the snapshot at the end proves that the puzzle position comes back exactly.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Puzzle on the demonstration board: promoting to a knight wins, and promoting to a queen stalemates. The teacher shows promotion in `make_move()` and `undo_move()`. |
| 3:15 to 3:45 | In `demo_promotion.py` student pairs write the loop that tries all four promotions and prints stalemate or checkmate for each. |
| 3:45 to 4:00 | The teacher hands out `uci_engine.py` and `remus.bat`. Student pairs register `remus.bat` from the period's `student` folder in Lucas Chess, following the [Lucas Chess guide](../../misc/docs/course/lucas_chess_guide.md). |
| 4:00 to 4:25 | Student pairs play their own Remus, which answers with random legal moves. Every special move works on a real board. |
| 4:25 to 4:30 | Checkpoint: every special-move test passes. |

## What you edit in the demo

Open `demo_promotion.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 12. Check the work by running `demo_promotion.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - Try All Four Promotions

```python
37 |     print("Part #1 - Try All Four Promotions")
38 |     # Predict first: which piece wins, and which ones only draw?
39 +     for letter in "QRBN":
40 +         move = Move(parse_square("b7"), parse_square("b8"), letter)
41 +         undo = make_move(state, move)
42 +         replies = len(legal_moves(state))
43 |         # No legal reply is checkmate if Black is in check, and stalemate if not
44 +         if replies > 0:
45 +             result = f"{replies} legal replies"
46 +         elif in_check(state, BLACK):
47 +             result = "checkmate"
48 +         else:
49 +             result = "stalemate"
50 +         print(f"  b8={letter}: {result}")
51 +         undo_move(state, undo)
52 |     print("  (expected stalemate for Q, R, and B, and checkmate for N)")
53 |
```

**How it works:** The loop tries all four promotions on b8, one after the other. For each one it makes the move, counts Black's legal replies, and decides the result. With no reply, a king in check is checkmated and a king not in check is stalemated. `undo_move` restores the position before the next promotion is tried.
