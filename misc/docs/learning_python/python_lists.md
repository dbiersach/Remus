# python_lists.py: A board is a list of rows

*Day 1, period 3. The lab file is `Day 01 - Draw the board/period3/student/python_lists.py`, and the answers are in `Day 01 - Draw the board/period3/instructor/python_lists_instructor.py`.*

## The big picture

Remus keeps the board as a list of 8 rows, and each row is a list of 8 squares. This
lab builds that board by hand: first one row of pieces, then all eight rows, then a
move that changes two squares.

## Where this piece fits

The lab does not import Remus. Part #3 builds the same 8x8 board that `new_board()`
in `board.py` returns on Day 1, period 4, with row 0 as rank 8.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](../code/board.md)

## Words to know

- **list:** values in order inside `[ ]`, such as the 8 pieces of a back rank.
- **len():** counts the items in a list.
- **for and range():** `for col in range(8)` runs the loop with col = 0, 1, ..., 7.
- **nested list:** a list whose items are lists. `board[row][col]` reads one square.

## How it works

1. Part #1: count the pieces of Black's back rank and read the piece on the d-file.
2. Part #2: print the back rank one piece at a time with a `for` loop.
3. Part #3: make 8 rows of dots, put in the pieces (row 0 is rank 8), and print the board.
4. Part #4: play 1. e4 by changing `board[6][4]` and `board[4][4]`, then count White's pawns on rank 2.

The student pair types 25 lines.

## Try it

Open `python_lists.py` in `Day 01 - Draw the board/period3/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 8 pieces, `q` on the d-file, the starting position with Black at the top, and 7 White pawns left on rank 2.

## Puzzle questions

1. Which `board[row][col]` holds the White king at the start?
2. Why does each row need its own new list of dots instead of one row used eight times?
