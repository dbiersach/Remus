# Day 5, Period 4: Promotion, and Remus plays in Lucas Chess

Register `remus.bat` from this folder as an engine in Lucas Chess and play your own Remus. It plays random legal moves, and every special move works.

## Learning objectives

By the end of this period, each pair can:

- Promote a pawn to any of four pieces. **Measured by:** The promotion tests pass for queen, rook, bishop, and knight.
- Explain why a player sometimes promotes to a knight. **Measured by:** Running `demo_promotion.py` prints stalemate for b8=Q, b8=R, and b8=B and checkmate for b8=N, and the pair says why the queen only draws.
- Play Remus in Lucas Chess. **Measured by:** The pair registers `remus.bat`, plays one game, and sees a random legal reply to every move, special moves included.

## The files

The demo is `demo_promotion.py` in the `student` folder, with the answers in `demo_promotion_instructor.py` in the `instructor` folder beside it. Open `demo_promotion.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `remus.bat`
- `uci_engine.py`

Files that grow this period:

- `make_move.py`
- `test_special_moves.py`

## The changes and why

The pairs fill in the blanks of `demo_promotion.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_promotion_instructor.py`.

`demo_promotion.py` sets up a puzzle: White's pawn on b7 promotes on b8 next to the Black king on a6. The pair writes the loop that tries all four promotion pieces, counts Black's legal replies, and names the result.

With no legal reply, `in_check()` decides between checkmate and stalemate. A queen, a rook, or a bishop takes away every square without giving check, so the game is a draw; only the knight on b8 gives check, and the king has nowhere to go. Every promotion is undone, and the snapshot at the end proves that the puzzle position comes back exactly.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit in the demo

Open `demo_promotion.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 12. Check the work by running `demo_promotion.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
