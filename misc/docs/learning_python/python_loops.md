# python_loops.py: Walk until something stops you

*Day 3, period 1. The lab file is `Day 03 - Generate piece moves/period1/student/python_loops.py`, and the answers are in `Day 03 - Generate piece moves/period1/instructor/python_loops_instructor.py`.*

## The big picture

A rook, a bishop, or a queen slides square by square until it reaches the edge of
the board or another piece. Nobody knows in advance how many steps that takes, so the
code uses a `while` loop and leaves it with `break`. This lab walks from d4 toward g7.

## Where this piece fits

The lab does not import Remus. On Day 3, period 3, `slide()` in `move_generation.py`
is the same walk, and it collects moves instead of square names.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`move_generation.py`](../engine_code/move_generation.md)

## Words to know

- **while:** repeats a block as long as its test is True.
- **break:** leaves the loop at once.
- **direction:** a tuple (row step, col step). Up and to the right is (-1, 1), because row 0 is rank 8.

## How it works

1. Part #1: count to 3 with `while`.
2. Part #2: unpack the direction `(-1, 1)` into a row step and a column step.
3. Part #3: step from d4 until the walk leaves the board or lands on a piece, and list each square.
4. Part #4: change the direction and run again.

The student pair types 14 lines.

## Try it

Open `python_loops.py` in `Day 03 - Generate piece moves/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: step 0, 1, 2; the steps -1 and 1; and the squares e5 f6 g7, where the Black pawn on g7 stops the walk.

## Puzzle questions

1. Why does the walk add g7 to the list before it stops?
2. Which direction tuple walks from d4 toward a1?
