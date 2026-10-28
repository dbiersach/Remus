# demo_promotion.py: Why a pawn becomes a knight

*Day 5, period 4. The demo file is `student/Day 05 - Add castling, en passant, and promotion/period4/demo_promotion.py`, and the answers are in `instructor/Day 05 - Add castling, en passant, and promotion/period4/demo_promotion_instructor.py`.*

## The big picture

A pawn that reaches the last rank may become a queen, a rook, a bishop, or a
knight. Nearly always the queen is best, but not here: White's pawn on b7 promotes on
b8, and a queen, a rook, or a bishop leaves Black's king with no move and no check.
That is stalemate, a draw. Only the knight gives check, and it is checkmate.

## Where this piece fits

The demo runs in the Day 5, period 4 folder and uses the promotion code the teacher
adds to `make_move.py` in this period, together with `legal_moves()` and `in_check()`.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`attacks.py`](attacks.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md)
- **Used by:** nothing; `test_special_moves.py` tests the four promotions

## Words to know

- **promotion:** a pawn on the last rank becomes another piece.
- **underpromotion:** promoting to a rook, a bishop, or a knight instead of a queen.
- **stalemate:** the side to move has no legal move and is not in check: the game is a draw.
- **checkmate:** the side to move has no legal move and is in check: the game is lost.

## How it works

1. `puzzle_state()` sets up White's king c6, bishop b6, and pawn b7 against Black's king a6.
2. Part #1: for each of Q, R, B, and N, make the promotion, count Black's replies, name the result, and undo the move.
3. Part #2: compare the state with a snapshot taken before Part #1.

The pair types 12 lines.

## Try it

Open `demo_promotion.py` in `student/Day 05 - Add castling, en passant, and promotion/period4` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: the puzzle board, stalemate for Q, R, and B, checkmate for N, and True for the snapshot.

## Puzzle questions

1. Which squares around a6 does the queen on b8 cover? Which square is left, and why can the king not go there?
2. Why does the knight give check from b8 when the queen does not?
